/*
 * The MIT License
 * 
 * Copyright (c) 2004-2009, Sun Microsystems, Inc., Kohsuke Kawaguchi, Fulvio Cavarretta,
 * Jean-Baptiste Quenot, Luca Domenico Milanesio, Renaud Bruyeron, Stephen Connolly,
 * Tom Huybrechts, Yahoo! Inc.
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
package hudson.scm;

import com.thoughtworks.xstream.XStream;
import com.trilead.ssh2.DebugLogger;
import com.trilead.ssh2.SCPClient;
import hudson.FilePath;
import hudson.FilePath.FileCallable;
import hudson.Launcher;
import hudson.Util;
import hudson.XmlFile;
import hudson.Functions;
import hudson.Extension;
import static hudson.Functions.defaulted;
import static hudson.Util.fixEmptyAndTrim;
import hudson.security.csrf.CrumbIssuer;
import hudson.model.AbstractBuild;
import hudson.model.AbstractProject;
import hudson.model.BuildListener;
import hudson.model.Hudson;
import hudson.model.ModelObject;
import hudson.model.ParametersAction;
import hudson.model.TaskListener;
import hudson.model.Run;
import hudson.model.Node;
import hudson.model.Computer;
import hudson.model.Hudson.MasterComputer;
import hudson.remoting.Callable;
import hudson.remoting.DelegatingCallable;
import hudson.remoting.Channel;
import hudson.remoting.VirtualChannel;
import hudson.scm.subversion.Messages;
import hudson.triggers.SCMTrigger;
import hudson.util.EditDistance;
import hudson.util.IOException2;
import hudson.util.MultipartFormDataParser;
import hudson.util.Scrambler;
import hudson.util.StreamCopyThread;
import hudson.util.XStream2;
import hudson.util.FormValidation;
import hudson.util.TimeUnit2;
import org.apache.commons.fileupload.FileItem;
import org.apache.commons.io.FileUtils;
import org.apache.commons.beanutils.PropertyUtils;
import org.apache.tools.ant.Project;
import org.apache.tools.ant.taskdefs.Chmod;
import org.kohsuke.stapler.StaplerRequest;
import org.kohsuke.stapler.StaplerResponse;
import org.kohsuke.stapler.QueryParameter;
import org.kohsuke.stapler.DataBoundConstructor;
import org.kohsuke.putty.PuTTYKey;
import org.tmatesoft.svn.core.SVNDirEntry;
import org.tmatesoft.svn.core.SVNErrorCode;
import org.tmatesoft.svn.core.SVNErrorMessage;
import org.tmatesoft.svn.core.SVNException;
import org.tmatesoft.svn.core.SVNNodeKind;
import org.tmatesoft.svn.core.SVNURL;
import org.tmatesoft.svn.core.SVNCancelException;
import org.tmatesoft.svn.core.ISVNLogEntryHandler;
import org.tmatesoft.svn.core.SVNLogEntry;
import org.tmatesoft.svn.core.SVNProperties;
import org.tmatesoft.svn.core.auth.ISVNAuthenticationManager;
import org.tmatesoft.svn.core.auth.ISVNAuthenticationProvider;
import org.tmatesoft.svn.core.auth.SVNAuthentication;
import org.tmatesoft.svn.core.auth.SVNPasswordAuthentication;
import org.tmatesoft.svn.core.auth.SVNSSHAuthentication;
import org.tmatesoft.svn.core.auth.SVNSSLAuthentication;
import org.tmatesoft.svn.core.auth.SVNUserNameAuthentication;
import org.tmatesoft.svn.core.internal.io.dav.DAVRepositoryFactory;
import org.tmatesoft.svn.core.internal.io.dav.http.DefaultHTTPConnectionFactory;
import org.tmatesoft.svn.core.internal.io.fs.FSRepositoryFactory;
import org.tmatesoft.svn.core.internal.io.svn.SVNRepositoryFactoryImpl;
import org.tmatesoft.svn.core.internal.util.SVNPathUtil;
import org.tmatesoft.svn.core.internal.wc.DefaultSVNAuthenticationManager;
import org.tmatesoft.svn.core.internal.wc.SVNErrorManager;
import org.tmatesoft.svn.core.internal.wc.SVNExternal;
import org.tmatesoft.svn.core.internal.wc.admin.SVNAdminAreaFactory;
import org.tmatesoft.svn.core.io.SVNCapability;
import org.tmatesoft.svn.core.io.SVNRepository;
import org.tmatesoft.svn.core.io.SVNRepositoryFactory;
import org.tmatesoft.svn.core.wc.SVNClientManager;
import org.tmatesoft.svn.core.wc.SVNInfo;
import org.tmatesoft.svn.core.wc.SVNRevision;
import org.tmatesoft.svn.core.wc.SVNUpdateClient;
import org.tmatesoft.svn.core.wc.SVNWCClient;
import org.tmatesoft.svn.core.wc.SVNWCUtil;
import org.tmatesoft.svn.core.wc.SVNLogClient;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletResponse;
import javax.xml.transform.stream.StreamResult;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.io.Serializable;
import java.io.StringWriter;
import java.io.PipedInputStream;
import java.io.PipedOutputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Random;
import java.util.Set;
import java.util.StringTokenizer;
import java.util.UUID;
import java.util.Iterator;
import java.util.logging.Level;
import java.util.logging.Logger;
import static java.util.logging.Level.FINE;
import java.util.regex.Pattern;
import java.util.regex.PatternSyntaxException;
import java.lang.reflect.InvocationTargetException;

import net.sf.json.JSONObject;

/**
 * Subversion SCM.
 *
 * <h2>Plugin Developer Notes</h2>
 * <p>
 * Plugins that interact with Subversion can use {@link DescriptorImpl#createAuthenticationProvider()}
 * so that it can use the credentials (username, password, etc.) that the user entered for Hudson.
 * See the javadoc of this method for the precautions you need to take if you run Subversion operations
 * remotely on slaves.
 * 
 * <h2>Implementation Notes</h2>
 * <p>
 * Because this instance refers to some other classes that are not necessarily
 * Java serializable (like {@link #browser}), remotable {@link FileCallable}s all
 * need to be declared as static inner classes.
 *
 * @author Kohsuke Kawaguchi
 */
public class SubversionSCM extends SCM implements Serializable {
    /**
     * the locations field is used to store all configured SVN locations (with
     * their local and remote part). Direct access to this filed should be
     * avoided and the getLocations() method should be used instead. This is
     * needed to make importing of old hudson-configurations possible as
     * getLocations() will check if the modules field has been set and import
     * the data.
     *
     * @since 1.91
     */
    private ModuleLocation[] locations = new ModuleLocation[0];

    private boolean useUpdate;
    private final SubversionRepositoryBrowser browser;
    private String excludedRegions;
    private String excludedUsers;
    private String excludedRevprop;
    private String excludedCommitMessages;

    // No longer in use but left for serialization compatibility.
    @Deprecated
    private String modules;

    /**
     * @deprecated as of 1.286
     */
    public SubversionSCM(String[] remoteLocations, String[] localLocations,
                         boolean useUpdate, SubversionRepositoryBrowser browser) {
        this(remoteLocations,localLocations, useUpdate, browser, null, null, null);
    }

    /**
     * @deprecated as of 1.311
     */
    public SubversionSCM(String[] remoteLocations, String[] localLocations,
                         boolean useUpdate, SubversionRepositoryBrowser browser, String excludedRegions) {
        this(ModuleLocation.parse(remoteLocations,localLocations), useUpdate, browser, excludedRegions, null, null, null);
    }

    /**
     * @deprecated as of 1.315
     */
     public SubversionSCM(String[] remoteLocations, String[] localLocations,
                         boolean useUpdate, SubversionRepositoryBrowser browser, String excludedRegions, String excludedUsers, String excludedRevprop) {
        this(ModuleLocation.parse(remoteLocations,localLocations), useUpdate, browser, excludedRegions, excludedUsers, excludedRevprop, null);
    }

   /**
     * @deprecated as of 1.315
     */
    public SubversionSCM(List<ModuleLocation> locations,
                         boolean useUpdate, SubversionRepositoryBrowser browser, String excludedRegions) {
        this(locations, useUpdate, browser, excludedRegions, null, null, null);
    }
    
    /**
     * @deprecated as of 1.324
     */
    public SubversionSCM(List<ModuleLocation> locations,
            boolean useUpdate, SubversionRepositoryBrowser browser, String excludedRegions, String excludedUsers, String excludedRevprop) {
        this(locations, useUpdate, browser, excludedRegions, excludedUsers, excludedRevprop, null);
    }

    @DataBoundConstructor
    public SubversionSCM(List<ModuleLocation> locations,
                         boolean useUpdate, SubversionRepositoryBrowser browser, String excludedRegions, String excludedUsers, String excludedRevprop, String excludedCommitMessages) {

        for (Iterator<ModuleLocation> itr = locations.iterator(); itr.hasNext();) {
            ModuleLocation ml = itr.next();
            if(ml.remote==null) itr.remove();
        }
        this.locations = locations.toArray(new ModuleLocation[locations.size()]);

        this.useUpdate = useUpdate;
        this.browser = browser;
        this.excludedRegions = excludedRegions;
        this.excludedUsers = excludedUsers;
        this.excludedRevprop = excludedRevprop;
        this.excludedCommitMessages = excludedCommitMessages;
    }

    /**
     * Convenience constructor, especially during testing.
     */
    public SubversionSCM(String svnUrl) {
        this(svnUrl,".");
    }

    /**
     * Convenience constructor, especially during testing.
     */
    public SubversionSCM(String svnUrl, String local) {
        this(new String[]{svnUrl},new String[]{local},true,null,null,null,null);
    }

    /**
     * @deprecated
     *      as of 1.91. Use {@link #getLocations()} instead.
     */
    public String getModules() {
        return null;
    }

    /**
     * list of all configured svn locations
     *
     * @since 1.91
     */
    public ModuleLocation[] getLocations() {
    	return getLocations(null);
    }
    
    /**
     * list of all configured svn locations, expanded according to 
     * build parameters values;
     *
     * @param build
     *      If non-null, variable expansions are performed against the build parameters.
     *
     * @since 1.252
     */
    public ModuleLocation[] getLocations(AbstractBuild<?,?> build) {
        // check if we've got a old location
        if (modules != null) {
            // import the old configuration
            List<ModuleLocation> oldLocations = new ArrayList<ModuleLocation>();
            StringTokenizer tokens = new StringTokenizer(modules);
            while (tokens.hasMoreTokens()) {
                // the remote (repository location)
                // the normalized name is always without the trailing '/'
                String remoteLoc = Util.removeTrailingSlash(tokens.nextToken());

                oldLocations.add(new ModuleLocation(remoteLoc, null));
            }

            locations = oldLocations.toArray(new ModuleLocation[oldLocations.size()]);
            modules = null;
        }

        if(build == null)
        	return locations;
        
        ModuleLocation[] outLocations = new ModuleLocation[locations.length];
        for (int i = 0; i < outLocations.length; i++) {
			outLocations[i] = locations[i].getExpandedLocation(build);
		}

        return outLocations;
    }

    public boolean isUseUpdate() {
        return useUpdate;
    }

    @Override
    public SubversionRepositoryBrowser getBrowser() {
        return browser;
    }

    public String getExcludedRegions() {
        return excludedRegions;
    }

    public String[] getExcludedRegionsNormalized() {
        return excludedRegions == null ? null : excludedRegions.split("[\\r\\n]+");
    }

    private Pattern[] getExcludedRegionsPatterns() {
        String[] excludedRegions = getExcludedRegionsNormalized();
        if (excludedRegions != null) {
            Pattern[] patterns = new Pattern[excludedRegions.length];

            int i = 0;
            for (String excludedRegion : excludedRegions) {
                patterns[i++] = Pattern.compile(excludedRegion);
            }

            return patterns;
        }

        return null;
    }

    public String getExcludedUsers() {
        return excludedUsers;
    }

    public String[] getExcludedUsersNormalized() {
        if (excludedUsers == null) {
            return null;
        }
        ArrayList<String> users = new ArrayList<String>();
        for (String user : excludedUsers.split("[\\r\\n]+")) {
            users.add(user.trim());
        }
        return users.toArray(new String[users.size()]);
    }

    public String getExcludedRevprop() {
        return excludedRevprop;
    }

    public String getExcludedCommitMessages() {
        return excludedCommitMessages;
    }

    public String[] getExcludedCommitMessagesNormalized() {
        return excludedCommitMessages == null ? new String[0] : excludedCommitMessages.split("[\\r\\n]+");
    }

    private Pattern[] getExcludedCommitMessagesPatterns() {
        String[] excludedCommitMessages = getExcludedCommitMessagesNormalized();
        Pattern[] patterns = new Pattern[excludedCommitMessages.length];

        int i = 0;
        for (String excludedCommitMessage : excludedCommitMessages) {
            patterns[i++] = Pattern.compile(excludedCommitMessage);
        }

        return patterns;
    }

    /**
     * Sets the <tt>SVN_REVISION</tt> environment variable during the build.
     */
    @Override
    public void buildEnvVars(AbstractBuild build, Map<String, String> env) {
        super.buildEnvVars(build, env);
        
        ModuleLocation[] locations = getLocations(build);

        try {
            Map<String,Long> revisions = parseRevisionFile(build);
            if(locations.length==1) {
                Long rev = revisions.get(locations[0].remote);
                if(rev!=null)
                    env.put("SVN_REVISION",rev.toString());
            }
            // it's not clear what to do if there are more than one modules.
            // if we always return locations[0].remote, it'll be difficult
            // to change this later (to something more sensible, such as
            // choosing the "root module" or whatever), so let's not set
            // anything for now.
            // besides, one can always use 'svnversion' to obtain the revision more explicitly.
        } catch (IOException e) {
            // ignore this error
        }
    }

    /**
     * Called after checkout/update has finished to compute the changelog.
     */
    private boolean calcChangeLog(AbstractBuild<?,?> build, File changelogFile, BuildListener listener, List<External> externals) throws IOException, InterruptedException {
        if(build.getPreviousBuild()==null) {
            // nothing to compare against
            return createEmptyChangeLog(changelogFile, listener, "log");
        }

        // some users reported that the file gets created with size 0. I suspect
        // maybe some XSLT engine doesn't close the stream properly.
        // so let's do it by ourselves to be really sure that the stream gets closed.
        OutputStream os = new BufferedOutputStream(new FileOutputStream(changelogFile));
        boolean created;
        try {
            created = new SubversionChangeLogBuilder(build, listener, this).run(externals, new StreamResult(os));
        } finally {
            os.close();
        }
        if(!created)
            createEmptyChangeLog(changelogFile, listener, "log");

        return true;
    }


    /**
     * Reads the revision file of the specified build.
     *
     * @return
     *      map from {@link SvnInfo#url Subversion URL} to its revision.
     */
    /*package*/ static Map<String,Long> parseRevisionFile(AbstractBuild build) throws IOException {
        Map<String,Long> revisions = new HashMap<String,Long>(); // module -> revision
        {// read the revision file of the last build
            File file = getRevisionFile(build);
            if(!file.exists())
                // nothing to compare against
                return revisions;

            BufferedReader br = new BufferedReader(new FileReader(file));
            try {
                String line;
                while((line=br.readLine())!=null) {
                    int index = line.lastIndexOf('/');
                    if(index<0) {
                        continue;   // invalid line?
                    }
                    try {
                        revisions.put(line.substring(0,index), Long.parseLong(line.substring(index+1)));
                    } catch (NumberFormatException e) {
                        // perhaps a corrupted line. ignore
                    }
                }
            } finally {
                br.close();
            }
        }

        return revisions;
    }

    /**
     * Parses the file that stores the locations in the workspace where modules loaded by svn:external
     * is placed.
     *
     * <p>
     * Note that the format of the file has changed in 1.180 from simple text file to XML.
     *
     * @return
     *      immutable list. Can be empty but never null.
     */
    /*package*/ static List<External> parseExternalsFile(AbstractProject project) throws IOException {
        File file = getExternalsFile(project);
        if(file.exists()) {
            try {
                return (List<External>)new XmlFile(External.XSTREAM,file).read();
            } catch (IOException e) {
                // in < 1.180 this file was a text file, so it may fail to parse as XML,
                // in which case let's just fall back
            }
        }

        return Collections.emptyList();
    }

    /**
     * Polling can happen on the master and does not require a workspace.
     */
    @Override
    public boolean requiresWorkspaceForPolling() {
        return false;
    }
    
    public boolean checkout(AbstractBuild build, Launcher launcher, FilePath workspace, final BuildListener listener, File changelogFile) throws IOException, InterruptedException {
        List<External> externals = checkout(build,workspace,listener);

        if(externals==null)
            return false;

        // write out the revision file
        PrintWriter w = new PrintWriter(new FileOutputStream(getRevisionFile(build)));
        try {
            Map<String,SvnInfo> revMap = workspace.act(new BuildRevisionMapTask(build, this, listener, externals));
            for (Entry<String,SvnInfo> e : revMap.entrySet()) {
                w.println( e.getKey() +'/'+ e.getValue().revision );
            }
            build.addAction(new SubversionTagAction(build,revMap.values()));
        } finally {
            w.close();
        }

        // write out the externals info
        new XmlFile(External.XSTREAM,getExternalsFile(build.getProject())).write(externals);

        return calcChangeLog(build, changelogFile, listener, externals);
    }

    /**
     * Performs the checkout or update, depending on the configuration and workspace state.
     *
     * <p>
     * Use canonical path to avoid SVNKit/symlink problem as described in
     * https://wiki.svnkit.com/SVNKit_FAQ
     *
     * @return null
     *      if the operation failed. Otherwise the set of local workspace paths
     *      (relative to the workspace root) that has loaded due to svn:external.
     */
    private List<External> checkout(AbstractBuild build, FilePath workspace, TaskListener listener) throws IOException, InterruptedException {
        if (repositoryLocationsNoLongerExist(build, listener)) {
            Run lsb = build.getProject().getLastSuccessfulBuild();
            if (lsb != null && build.getNumber()-lsb.getNumber()>10
            && build.getTimestamp().getTimeInMillis()-lsb.getTimestamp().getTimeInMillis() > TimeUnit2.DAYS.toMillis(1)) {
                // Disable this project if the location doesn't exist any more, see issue #763
                // but only do so if there was at least some successful build,
                // to make sure that initial configuration error won't disable the build. see issue #1567
                // finally, only disable a build if the failure persists for some time.
                // see http://www.nabble.com/Should-Hudson-have-an-option-for-a-content-fingerprint--td24022683.html

                listener.getLogger().println("One or more repository locations do not exist anymore for " + build.getProject().getName() + ", project will be disabled.");
                build.getProject().makeDisabled(true);
                return null;
            }
        }

        Boolean isUpdatable = useUpdate && workspace.act(new IsUpdatableTask(build, this, listener));
        return workspace.act(new CheckOutTask(build, this, build.getTimestamp().getTime(), isUpdatable, listener));
    }


    /**
     * Either run "svn co" or "svn up" equivalent.
     */
    private static class CheckOutTask implements FileCallable<List<External>> {
        private final ISVNAuthenticationProvider authProvider;
        private final Date timestamp;
        // true to "svn update", false to "svn checkout".
        private boolean update;
        private final TaskListener listener;
        private final ModuleLocation[] locations;
        private final RevisionParameterAction revisions;

        public CheckOutTask(AbstractBuild<?, ?> build, SubversionSCM parent, Date timestamp, boolean update, TaskListener listener) {
            this.authProvider = parent.getDescriptor().createAuthenticationProvider();
            this.timestamp = timestamp;
            this.update = update;
            this.listener = listener;
            this.locations = parent.getLocations(build);
            revisions = build.getAction(RevisionParameterAction.class);
        }

        public List<External> invoke(File ws, VirtualChannel channel) throws IOException {
            final SVNClientManager manager = createSvnClientManager(authProvider);
            try {
                final SVNUpdateClient svnuc = manager.getUpdateClient();
                final List<External> externals = new ArrayList<External>(); // store discovered externals to here
                if(update) {
                    for (final ModuleLocation l : locations) {
                        try {
                            listener.getLogger().println("Updating "+ l.remote);

                            File local = new File(ws, l.getLocalDir());
                            svnuc.setEventHandler(new SubversionUpdateEventHandler(listener.getLogger(), externals,local,l.getLocalDir()));
                            
                            SVNRevision r = getRevision(l);
                            
                            svnuc.doUpdate(local.getCanonicalFile(), r, true);

                        } catch (final SVNException e) {
                            if(e.getErrorMessage().getErrorCode()== SVNErrorCode.WC_LOCKED) {
                                // work space locked. try fresh check out
                                listener.getLogger().println("Workspace appear to be locked, so getting a fresh workspace");
                                update = false;
                                return invoke(ws,channel);
                            }
                            if(e.getErrorMessage().getErrorCode()== SVNErrorCode.WC_OBSTRUCTED_UPDATE) {
                                // HUDSON-1882. If existence of local files cause an update to fail,
                                // revert to fresh check out
                                listener.getLogger().println(e.getMessage()); // show why this happened. Sometimes this is caused by having a build artifact in the repository.
                                listener.getLogger().println("Updated failed due to local files. Getting a fresh workspace");
                                update = false;
                                return invoke(ws,channel);
                            }

                            e.printStackTrace(listener.error("Failed to update "+l.remote));
                            // trouble-shooting probe for #591
                            if(e.getErrorMessage().getErrorCode()== SVNErrorCode.WC_NOT_LOCKED) {
                                listener.getLogger().println("Polled jobs are "+ Hudson.getInstance().getDescriptorByType(SCMTrigger.DescriptorImpl.class).getItemsBeingPolled());
                            }
                            return null;
                        }
                    }
                } else {
                    Util.deleteContentsRecursive(ws);

                    // buffer the output by a separate thread so that the update operation
                    // won't be blocked by the remoting of the data
                    PipedOutputStream pos = new PipedOutputStream();
                    StreamCopyThread sct = new StreamCopyThread("svn log copier", new PipedInputStream(pos), listener.getLogger());
                    sct.start();

                    for (final ModuleLocation l : locations) {
                        try {
                            listener.getLogger().println("Checking out "+l.remote);

                            File local = new File(ws, l.getLocalDir());
                            svnuc.setEventHandler(new SubversionUpdateEventHandler(new PrintStream(pos), externals, local, l.getLocalDir()));
                            svnuc.doCheckout(l.getSVNURL(), local.getCanonicalFile(), SVNRevision.HEAD, getRevision(l), true);
                        } catch (SVNException e) {
                            e.printStackTrace(listener.error("Failed to check out "+l.remote));
                            return null;
                        }
                    }
                    
                    pos.close();
                    try {
						sct.join(); // wait for all data to be piped.
					} catch (InterruptedException e) {
                        throw new IOException2("interrupted",e);
                    }
                }

                try {
                    for (final ModuleLocation l : locations) {
                        SVNDirEntry dir = manager.createRepository(l.getSVNURL(),true).info("/",-1);
                        if(dir!=null) {// I don't think this can ever be null, but be defensive
                            if(dir.getDate()!=null && dir.getDate().after(new Date())) // see http://www.nabble.com/NullPointerException-in-SVN-Checkout-Update-td21609781.html that reported this being null.
                                listener.getLogger().println(Messages.SubversionSCM_ClockOutOfSync());
                        }
                    }
                } catch (SVNException e) {
                    LOGGER.log(Level.INFO,"Failed to estimate the remote time stamp",e);
                }

                return externals;
            } finally {
                manager.dispose();
            }
        }

		private SVNRevision getRevision(ModuleLocation l) {
			// for the SVN revision, we will use the first off:
			// - a @NNN prefix of the SVN url
			// - a value found in a RevisionParameterAction
			// - the revision corresponding to the build timestamp
			
			SVNRevision r = null;
			if (revisions != null) {
				r = revisions.getRevision(l.getURL());
			}
			if (r == null) {
                r = SVNRevision.create(timestamp);
			}
			r = l.getRevision(r);
			return r;
		}

        private static final long serialVersionUID = 1L;
    }

    /**
     * Creates {@link SVNClientManager}.
     *
     * <p>
     * This method must be executed on the slave where svn operations are performed.
     *
     * @param authProvider
     *      The value obtained from {@link DescriptorImpl#createAuthenticationProvider()}.
     *      If the operation runs on slaves,
     *      (and properly remoted, if the svn operations run on slaves.)
     */
    public static SVNClientManager createSvnClientManager(ISVNAuthenticationProvider authProvider) {
        ISVNAuthenticationManager sam = SVNWCUtil.createDefaultAuthenticationManager();
        sam.setAuthenticationProvider(authProvider);
        return SVNClientManager.newInstance(SVNWCUtil.createDefaultOptions(true),sam);
    }

    /**
     * Creates {@link SVNClientManager} for code running on the master.
     * <p>
     * CAUTION: this code only works when invoked on master. On slaves, use
     * {@link #createSvnClientManager(ISVNAuthenticationProvider)} and get {@link ISVNAuthenticationProvider}
     * from the master via remoting. 
     */
    public static SVNClientManager createSvnClientManager() {
        return createSvnClientManager(Hudson.getInstance().getDescriptorByType(DescriptorImpl.class).createAuthenticationProvider());
    }

    public static final class SvnInfo implements Serializable, Comparable<SvnInfo> {
        /**
         * Decoded repository URL.
         */
        public final String url;
        public final long revision;

        public SvnInfo(String url, long revision) {
            this.url = url;
            this.revision = revision;
        }

        public SvnInfo(SVNInfo info) {
            this( info.getURL().toDecodedString(), info.getCommittedRevision().getNumber() );
        }

        public SVNURL getSVNURL() throws SVNException {
            return SVNURL.parseURIDecoded(url);
        }

        public int compareTo(SvnInfo that) {
            int r = this.url.compareTo(that.url);
            if(r!=0)    return r;

            if(this.revision<that.revision) return -1;
            if(this.revision>that.revision) return +1;
            return 0;
        }

        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;

            SvnInfo svnInfo = (SvnInfo) o;

            if (revision != svnInfo.revision) return false;
            return url.equals(svnInfo.url);

        }

        public int hashCode() {
            int result;
            result = url.hashCode();
            result = 31 * result + (int) (revision ^ (revision >>> 32));
            return result;
        }

        public String toString() {
            return String.format("%s (rev.%s)",url,revision);
        }

        private static final long serialVersionUID = 1L;
    }

    /**
     * Information about svn:external
     */
    static final class External implements Serializable {
        /**
         * Relative path within the workspace where this <tt>svn:exteranls</tt> exist. 
         */
        final String path;

        /**
         * External SVN URL to be fetched.
         */
        final String url;

        /**
         * If the svn:external link is with the -r option, its number.
         * Otherwise -1 to indicate that the head revision of the external repository should be fetched.
         */
        final long revision;

        /**
         * @param modulePath
         *      The root of the current module that svn was checking out when it hits 'ext'.
         *      Since we call svnkit multiple times in general case to check out from multiple locations,
         *      we use this to make the path relative to the entire workspace, not just the particular module.
         */
        External(String modulePath,SVNExternal ext) {
            this.path = modulePath+'/'+ext.getPath();
            this.url = ext.getResolvedURL().toDecodedString();
            this.revision = ext.getRevision().getNumber();
        }

        /**
         * Returns true if this reference is to a fixed revision.
         */
        boolean isRevisionFixed() {
            return revision!=-1;
        }

        private static final long serialVersionUID = 1L;

        private static final XStream XSTREAM = new XStream2();
        static {
            XSTREAM.alias("external",External.class);
        }
    }

    /**
     * Gets the SVN metadata for the given local workspace.
     *
     * @param workspace
     *      The target to run "svn info".
     */
    private static SVNInfo parseSvnInfo(File workspace, ISVNAuthenticationProvider authProvider) throws SVNException {
        final SVNClientManager manager = createSvnClientManager(authProvider);
        try {
            final SVNWCClient svnWc = manager.getWCClient();
            return svnWc.doInfo(workspace,SVNRevision.WORKING);
        } finally {
            manager.dispose();
        }
    }

    /**
     * Gets the SVN metadata for the remote repository.
     *
     * @param remoteUrl
     *      The target to run "svn info".
     */
    private static SVNInfo parseSvnInfo(SVNURL remoteUrl, ISVNAuthenticationProvider authProvider) throws SVNException {
        final SVNClientManager manager = createSvnClientManager(authProvider);
        try {
            final SVNWCClient svnWc = manager.getWCClient();
            return svnWc.doInfo(remoteUrl, SVNRevision.HEAD, SVNRevision.HEAD);
        } finally {
            manager.dispose();
        }
    }

    /**
     * Checks .svn files in the workspace and finds out revisions of the modules
     * that the workspace has.
     *
     * @return
     *      null if the parsing somehow fails. Otherwise a map from the repository URL to revisions.
     */
    private static class BuildRevisionMapTask implements FileCallable<Map<String,SvnInfo>> {
        private final ISVNAuthenticationProvider authProvider;
        private final TaskListener listener;
        private final List<External> externals;
        private final ModuleLocation[] locations;

        public BuildRevisionMapTask(AbstractBuild<?, ?> build, SubversionSCM parent, TaskListener listener, List<External> externals) {
            this.authProvider = parent.getDescriptor().createAuthenticationProvider();
            this.listener = listener;
            this.externals = externals;
            this.locations = parent.getLocations(build);
        }

        public Map<String,SvnInfo> invoke(File ws, VirtualChannel channel) throws IOException {
            Map<String/*module name*/,SvnInfo> revisions = new HashMap<String,SvnInfo>();

            final SVNClientManager manager = createSvnClientManager(authProvider);
            try {
                final SVNWCClient svnWc = manager.getWCClient();
                // invoke the "svn info"
                for( ModuleLocation module : locations ) {
                    try {
                        SvnInfo info = new SvnInfo(svnWc.doInfo(new File(ws,module.getLocalDir()), SVNRevision.WORKING));
                        revisions.put(info.url,info);
                    } catch (SVNException e) {
                        e.printStackTrace(listener.error("Failed to parse svn info for "+module.remote));
                    }
                }
                for(External ext : externals){
                    try {
                        SvnInfo info = new SvnInfo(svnWc.doInfo(new File(ws,ext.path),SVNRevision.WORKING));
                        revisions.put(info.url,info);
                    } catch (SVNException e) {
                        e.printStackTrace(listener.error("Failed to parse svn info for external "+ext.url+" at "+ext.path));
                    }

                }

                return revisions;
            } finally {
                manager.dispose();
            }
        }
        private static final long serialVersionUID = 1L;
    }

    /**
     * Gets the file that stores the revision.
     */
    public static File getRevisionFile(AbstractBuild build) {
        return new File(build.getRootDir(),"revision.txt");
    }

    /**
     * Gets the file that stores the externals.
     */
    private static File getExternalsFile(AbstractProject project) {
        return new File(project.getRootDir(),"svnexternals.txt");
    }

    /**
     * Returns true if we can use "svn update" instead of "svn checkout"
     */
    private static class IsUpdatableTask implements FileCallable<Boolean> {
        private final TaskListener listener;
        private final ISVNAuthenticationProvider authProvider;
        private final ModuleLocation[] locations;

        IsUpdatableTask(AbstractBuild<?, ?> build, SubversionSCM parent,TaskListener listener) {
            this.authProvider = parent.getDescriptor().createAuthenticationProvider();
            this.listener = listener;
            this.locations = parent.getLocations(build);
        }

        public Boolean invoke(File ws, VirtualChannel channel) throws IOException {
            for (ModuleLocation l : locations) {
                String moduleName = l.getLocalDir();
                File module = new File(ws,moduleName).getCanonicalFile(); // canonicalize to remove ".." and ".". See #474

                if(!module.exists()) {
                    listener.getLogger().println("Checking out a fresh workspace because "+module+" doesn't exist");
                    return false;
                }

                try {
                    SVNInfo svnkitInfo = parseSvnInfo(module, authProvider);
                    SvnInfo svnInfo = new SvnInfo(svnkitInfo);

                    String url = l.getURL();
                    if(!svnInfo.url.equals(url)) {
                        listener.getLogger().println("Checking out a fresh workspace because the workspace is not "+url);
                        return false;
                    }
                } catch (SVNException e) {
                    if (e.getErrorMessage().getErrorCode()==SVNErrorCode.WC_NOT_DIRECTORY) {
                        listener.getLogger().println("Checking out a fresh workspace because there's no workspace at "+module);
                    } else {
                        listener.getLogger().println("Checking out a fresh workspace because Hudson failed to detect the current workspace "+module);
                        e.printStackTrace(listener.error(e.getMessage()));
                    }
                    return false;
                }
            }
            return true;
        }
        private static final long serialVersionUID = 1L;
    }

    public boolean pollChanges(AbstractProject project, Launcher launcher,
            FilePath workspace, final TaskListener listener) throws IOException,
            InterruptedException {
        AbstractBuild lastBuild = (AbstractBuild) project.getLastBuild();
        if (lastBuild == null) {
            listener.getLogger().println(
                    "No existing build. Starting a new one");
            return true;
        }

        if (repositoryLocationsNoLongerExist(lastBuild, listener)) {
            // Disable this project, see issue #763

            listener.getLogger().println(
                    "One or more repository locations do not exist anymore for "
                            + project + ", project will be disabled.");
            project.makeDisabled(true);
            return false;
        }

        // current workspace revision
        final Map<String,Long> wsRev = parseRevisionFile(lastBuild);
        final List<External> externals = parseExternalsFile(project);

        // First check to see if the lastBuild is still running - if it is, we skip this next section,
        // to deal with https://hudson.dev.java.net/issues/show_bug.cgi?id=4270.
        if (!lastBuild.isBuilding()) {
            // are the locations checked out in the workspace consistent with the current configuration?
            for (ModuleLocation loc : getLocations(lastBuild)) {
                if (!wsRev.containsKey(loc.getURL())) {
                    listener.getLogger().println("Workspace doesn't contain " + loc.getURL() + ". Need a new build");
                    return true;
                }
            }
        }

        // determine where to perform polling. prefer the node where the build happened,
        // in case a cluster is non-uniform. see http://www.nabble.com/svn-connection-from-slave-only-td24970587.html
        VirtualChannel ch=null;
        Node n = lastBuild.getBuiltOn();
        if (n!=null) {
            Computer c = n.toComputer();
            if (c!=null)    ch = c.getChannel();
        }
        if (ch==null)   ch= MasterComputer.localChannel;
        
        // check the corresponding remote revision
        return ch.call(new DelegatingCallable<Boolean,IOException> () {
            final ISVNAuthenticationProvider authProvider = getDescriptor().createAuthenticationProvider();
            final String globalExcludedRevprop = getDescriptor().getGlobalExcludedRevprop();
            
            public ClassLoader getClassLoader() {
                return Hudson.getInstance().getPluginManager().uberClassLoader;
            }
        	
            public Boolean call() throws IOException {
                OUTER:
                for (Map.Entry<String,Long> localInfo : wsRev.entrySet()) {
                    // skip if this is an external reference to a fixed revision
                    String url = localInfo.getKey();

                    for (External ext : externals)
                        if(ext.url.equals(url) && ext.isRevisionFixed())
                            continue OUTER;

                    try {
                        final SVNURL decodedURL = SVNURL.parseURIDecoded(url);
                        SvnInfo remoteInfo = new SvnInfo(parseSvnInfo(decodedURL,authProvider));
                        listener.getLogger().println(Messages.SubversionSCM_pollChanges_remoteRevisionAt(url,remoteInfo.revision));
                        if(remoteInfo.revision > localInfo.getValue()) {
                            boolean changesFound = true;
                            Pattern[] excludedPatterns = getExcludedRegionsPatterns();
                            String[] excludedUsers = getExcludedUsersNormalized();
                            String excludedRevprop = defaulted(fixEmptyAndTrim(getExcludedRevprop()),globalExcludedRevprop);
                            Pattern[] excludedCommitMessages = getExcludedCommitMessagesPatterns();

                            if (excludedPatterns != null || excludedUsers != null || excludedRevprop != null || excludedCommitMessages.length>0) {
                                SVNLogHandler handler = new SVNLogHandler(listener, excludedPatterns, excludedUsers, excludedRevprop, excludedCommitMessages);
                                final SVNClientManager manager = createSvnClientManager(authProvider);
                                try {
                                    final SVNLogClient svnlc = manager.getLogClient();
                                    svnlc.doLog(decodedURL, null, SVNRevision.UNDEFINED,
                                            SVNRevision.create(localInfo.getValue() + 1), // get log entries from the local revision + 1
                                            SVNRevision.create(remoteInfo.revision), // to the remote revision
                                            false, // Don't stop on copy.
                                            true, // Report paths.
                                            false, // Don't included merged revisions
                                            0, // Retrieve log entries for unlimited number of revisions.
                                            null, // Retrieve all revprops
                                            handler);
                                } finally {
                                    manager.dispose();
                                }

                                changesFound = handler.isChangesFound();
                            }

                            if (changesFound) {
                                listener.getLogger().println(Messages.SubversionSCM_pollChanges_changedFrom(localInfo.getValue()));
                                return true;
                            }
                        }
                    } catch (SVNException e) {
                        e.printStackTrace(listener.error("Failed to check repository revision for "+ url));
                    }
                }
                return false; // no change
            }
        });
    }

    private final class SVNLogHandler implements ISVNLogEntryHandler {
         private boolean changesFound = false;

         private TaskListener listener;
	 private Pattern[] excludedPatterns;
         private HashSet<String> excludedUsers;
         private String excludedRevprop;
         private Pattern[] excludedCommitMessages;

         private SVNLogHandler(TaskListener listener, Pattern[] excludedPatterns, String[] excludedUsers, String excludedRevprop, Pattern[] excludedCommitMessages) {
             this.listener = listener;
             this.excludedPatterns = excludedPatterns == null ? new Pattern[0] : excludedPatterns;
             this.excludedUsers = new HashSet<String>(Arrays.asList(excludedUsers == null ? new String[0] : excludedUsers));
             this.excludedRevprop = excludedRevprop;
             this.excludedCommitMessages = excludedCommitMessages == null ? new Pattern[0] : excludedCommitMessages;
         }

         public boolean isChangesFound() {
            return changesFound;
	}

         /**
          * Handles a log entry passed.
          * Check for log entries that should be excluded from triggering a build.
          * If an entry is not an entry that should be excluded, set changesFound to true
          *
          * @param logEntry an {@link org.tmatesoft.svn.core.SVNLogEntry} object
          *                 that represents per revision information
          *                 (committed paths, log message, etc.)
          * @throws org.tmatesoft.svn.core.SVNException
          */
        public void handleLogEntry(SVNLogEntry logEntry) throws SVNException {
            if (checkLogEntry(logEntry)) {
                changesFound = true;
            }
        }

        /**
         * Checks if the given log entry should be considered for the purposes
         * of SCM polling.
         *
         * @return <code>true</code> if the should trigger polling, <code>false</code> otherwise
         */
        private boolean checkLogEntry(SVNLogEntry logEntry) {
            if (excludedRevprop != null) {
                // If the entry includes the exclusion revprop, don't count it as a change
                SVNProperties revprops = logEntry.getRevisionProperties();
                if (revprops != null && revprops.containsName(excludedRevprop)) {
                    listener.getLogger().println(Messages.SubversionSCM_pollChanges_ignoredRevision(
                            logEntry.getRevision(),
                            Messages.SubversionSCM_pollChanges_ignoredRevision_revprop(excludedRevprop)));
                    return false;
                }
            }

            String author = logEntry.getAuthor();
            if (excludedUsers.contains(author)) {
                // If the author is an excluded user, don't count this entry as a change
                listener.getLogger().println(Messages.SubversionSCM_pollChanges_ignoredRevision(
                        logEntry.getRevision(),
                        Messages.SubversionSCM_pollChanges_ignoredRevision_author(author)));
                return false;
            }

            if (excludedCommitMessages != null) {
                // If the commit message contains one of the excluded messages, don't count it as a change
                String commitMessage = logEntry.getMessage();
                for (Pattern pattern : excludedCommitMessages) {
                    if (pattern.matcher(commitMessage).find()) {
                        return false;
                    }
                }
            }

            // If there were no changes, don't count this entry as a change
            Map changedPaths = logEntry.getChangedPaths();
            if (changedPaths.isEmpty()) {
                return false;
            }

            // Else, check each changed path
            List<String> excludedPaths = new ArrayList<String>();
            for (String path : (Set<String>)changedPaths.keySet()) {
                for (Pattern pattern : excludedPatterns) {
                    if (pattern.matcher(path).matches()) {
                        excludedPaths.add(path);
                        break;
                    }
                }
            }

            // If all paths are in an excluded region, don't count this entry as a change
            if (changedPaths.size() == excludedPaths.size()) {
                listener.getLogger().println(Messages.SubversionSCM_pollChanges_ignoredRevision(
                        logEntry.getRevision(),
                        Messages.SubversionSCM_pollChanges_ignoredRevision_path(Util.join(excludedPaths, ", "))));
                return false;
            }

            // Otherwise, a change is a change
            return true;
        }
    }

    public ChangeLogParser createChangeLogParser() {
        return new SubversionChangeLogParser();
    }


    public DescriptorImpl getDescriptor() {
        return (DescriptorImpl)super.getDescriptor();
    }

    public FilePath getModuleRoot(FilePath workspace) {
        if (getLocations().length > 0)
            return workspace.child(getLocations()[0].getLocalDir());
        return workspace;
    }

    public FilePath[] getModuleRoots(FilePath workspace) {
        final ModuleLocation[] moduleLocations = getLocations();
        if (moduleLocations.length > 0) {
            FilePath[] moduleRoots = new FilePath[moduleLocations.length];
            for (int i = 0; i < moduleLocations.length; i++) {
                moduleRoots[i] = workspace.child(moduleLocations[i].getLocalDir());
            }
            return moduleRoots;
        }
        return new FilePath[] { getModuleRoot(workspace) };
    }

    private static String getLastPathComponent(String s) {
        String[] tokens = s.split("/");
        return tokens[tokens.length-1]; // return the last token
    }

    @Extension
    public static class DescriptorImpl extends SCMDescriptor<SubversionSCM> implements ModelObject {
        /**
         * SVN authentication realm to its associated credentials.
         */
        private final Map<String,Credential> credentials = new Hashtable<String,Credential>();

        /**
         * Stores name of Subversion revision property to globally exclude
         */
        private String globalExcludedRevprop = null;

        /**
         * Stores whether a realm supports revision properties
         */
        private final Map<String,Boolean> revPropSupport = new Hashtable<String,Boolean>();
        
        /**
         * Stores {@link SVNAuthentication} for a single realm.
         *
         * <p>
         * {@link Credential} holds data in a persistence-friendly way,
         * and it's capable of creating {@link SVNAuthentication} object,
         * to be passed to SVNKit.
         */
        public static abstract class Credential implements Serializable {
            /**
             * @param kind
             *      One of the constants defined in {@link ISVNAuthenticationManager},
             *      indicating what subype of {@link SVNAuthentication} is expected.
             */
            public abstract SVNAuthentication createSVNAuthentication(String kind) throws SVNException;
        }

        /**
         * Username/password based authentication.
         */
        private static final class PasswordCredential extends Credential {
            private final String userName;
            private final String password; // scrambled by base64

            public PasswordCredential(String userName, String password) {
                this.userName = userName;
                this.password = Scrambler.scramble(password);
            }

            @Override
            public SVNAuthentication createSVNAuthentication(String kind) {
                if(kind.equals(ISVNAuthenticationManager.SSH))
                    return new SVNSSHAuthentication(userName,Scrambler.descramble(password),-1,false);
                else
                    return new SVNPasswordAuthentication(userName,Scrambler.descramble(password),false);
            }
        }

        /**
         * Publickey authentication for Subversion over SSH.
         */
        private static final class SshPublicKeyCredential extends Credential {
            private final String userName;
            private final String passphrase; // scrambled by base64
            private final String id;

            /**
             * @param keyFile
             *      stores SSH private key. The file will be copied.
             */
            public SshPublicKeyCredential(String userName, String passphrase, File keyFile) throws SVNException {
                this.userName = userName;
                this.passphrase = Scrambler.scramble(passphrase);

                Random r = new Random();
                StringBuilder buf = new StringBuilder();
                for(int i=0;i<16;i++)
                    buf.append(Integer.toHexString(r.nextInt(16)));
                this.id = buf.toString();

                try {
                    FileUtils.copyFile(keyFile,getKeyFile());
                } catch (IOException e) {
                    throw new SVNException(SVNErrorMessage.create(SVNErrorCode.AUTHN_CREDS_UNAVAILABLE,"Unable to save private key"),e);
                }
            }

            /**
             * Gets the location where the private key will be permanently stored.
             */
            private File getKeyFile() {
                File dir = new File(Hudson.getInstance().getRootDir(),"subversion-credentials");
                if(dir.mkdirs()) {
                    // make sure the directory exists. if we created it, try to set the permission to 600
                    // since this is sensitive information
                    try {
                        Chmod chmod = new Chmod();
                        chmod.setProject(new Project());
                        chmod.setFile(dir);
                        chmod.setPerm("600");
                        chmod.execute();
                    } catch (Throwable e) {
                        // if we failed to set the permission, that's fine.
                        LOGGER.log(Level.WARNING, "Failed to set directory permission of "+dir,e);
                    }
                }
                return new File(dir,id);
            }

            @Override
            public SVNSSHAuthentication createSVNAuthentication(String kind) throws SVNException {
                if(kind.equals(ISVNAuthenticationManager.SSH)) {
                    try {
                        Channel channel = Channel.current();
                        String privateKey;
                        if(channel!=null) {
                            // remote
                            privateKey = channel.call(new Callable<String,IOException>() {
                                public String call() throws IOException {
                                    return FileUtils.readFileToString(getKeyFile(),"iso-8859-1");
                                }
                            });
                        } else {
                            privateKey = FileUtils.readFileToString(getKeyFile(),"iso-8859-1");
                        }
                        return new SVNSSHAuthentication(userName, privateKey.toCharArray(), Scrambler.descramble(passphrase),-1,false);
                    } catch (IOException e) {
                        throw new SVNException(SVNErrorMessage.create(SVNErrorCode.AUTHN_CREDS_UNAVAILABLE,"Unable to load private key"),e);
                    } catch (InterruptedException e) {
                        throw new SVNException(SVNErrorMessage.create(SVNErrorCode.AUTHN_CREDS_UNAVAILABLE,"Unable to load private key"),e);
                    }
                } else
                    return null; // unknown
            }
        }

        /**
         * SSL client certificate based authentication.
         */
        private static final class SslClientCertificateCredential extends Credential {
            private final String password; // scrambled by base64

            public SslClientCertificateCredential(File certificate, String password) {
                this.password = Scrambler.scramble(password);
            }

            @Override
            public SVNAuthentication createSVNAuthentication(String kind) {
                if(kind.equals(ISVNAuthenticationManager.SSL))
                    return new SVNSSLAuthentication(null,Scrambler.descramble(password),false);
                else
                    return null; // unexpected authentication type
            }
        }

        /**
         * Remoting interface that allows remote {@link ISVNAuthenticationProvider}
         * to read from local {@link DescriptorImpl#credentials}.
         */
        private interface RemotableSVNAuthenticationProvider {
            Credential getCredential(SVNURL url, String realm);
        }

        /**
         * There's no point in exporting multiple {@link RemotableSVNAuthenticationProviderImpl} instances,
         * so let's just use one instance.
         */
        private transient final RemotableSVNAuthenticationProviderImpl remotableProvider = new RemotableSVNAuthenticationProviderImpl();

        private final class RemotableSVNAuthenticationProviderImpl implements RemotableSVNAuthenticationProvider, Serializable {
            public Credential getCredential(SVNURL url, String realm) {
                for (SubversionCredentialProvider p : SubversionCredentialProvider.all()) {
                    Credential c = p.getCredential(url,realm);
                    if(c!=null) {
                        LOGGER.fine(String.format("getCredential(%s)=>%s by %s",realm,c,p));
                        return c;
                    }
                }
                LOGGER.fine(String.format("getCredential(%s)=>%s",realm,credentials.get(realm)));
                return credentials.get(realm);
            }

            /**
             * When sent to the remote node, send a proxy.
             */
            private Object writeReplace() {
                return Channel.current().export(RemotableSVNAuthenticationProvider.class, this);
            }
        }

        /**
         * See {@link DescriptorImpl#createAuthenticationProvider()}.
         */
        private static final class SVNAuthenticationProviderImpl implements ISVNAuthenticationProvider, Serializable {
            private final RemotableSVNAuthenticationProvider source;

            public SVNAuthenticationProviderImpl(RemotableSVNAuthenticationProvider source) {
                this.source = source;
            }

            public SVNAuthentication requestClientAuthentication(String kind, SVNURL url, String realm, SVNErrorMessage errorMessage, SVNAuthentication previousAuth, boolean authMayBeStored) {
                Credential cred = source.getCredential(url,realm);
                LOGGER.fine(String.format("requestClientAuthentication(%s,%s,%s)=>%s",kind,url,realm,cred));

                try {
                    SVNAuthentication auth=null;
                    if(cred!=null)
                        auth = cred.createSVNAuthentication(kind);

                    if(previousAuth!=null && compareSVNAuthentications(auth,previousAuth)) {
                        // See HUDSON-2909
                        // this comparison is necessary, unlike the original fix of HUDSON-2909, since SVNKit may use
                        // other ISVNAuthenticationProviders and their failed auth might be passed to us.
                        // see HUDSON-3936
                        LOGGER.fine("Previous authentication attempt failed, so aborting: "+previousAuth);
                        return null;
                    }

                    if(auth==null && ISVNAuthenticationManager.USERNAME.equals(kind)) {
                        // this happens with file:// URL and svn+ssh (in this case this method gets invoked twice.)
                        // The base class does this, too.
                        // user auth shouldn't be null.
                        return new SVNUserNameAuthentication("",false);
                    }

                    return auth;
                } catch (SVNException e) {
                    LOGGER.log(Level.SEVERE, "Failed to authorize",e);
                    throw new RuntimeException("Failed to authorize",e);
                }
            }

            public int acceptServerAuthentication(SVNURL url, String realm, Object certificate, boolean resultMayBeStored) {
                return ACCEPTED_TEMPORARY;
            }

            private static final long serialVersionUID = 1L;
        }

        @Override
        public SCM newInstance(StaplerRequest staplerRequest, JSONObject jsonObject) throws FormException {
            return super.newInstance(staplerRequest, jsonObject);
        }

        public DescriptorImpl() {
            super(SubversionRepositoryBrowser.class);
            load();
        }

        protected DescriptorImpl(Class clazz, Class<? extends RepositoryBrowser> repositoryBrowser) {
            super(clazz,repositoryBrowser);
        }

        public String getDisplayName() {
            return "Subversion";
        }

        public String getGlobalExcludedRevprop() {
            return globalExcludedRevprop;
        }

        @Override
        public boolean configure(StaplerRequest req) throws FormException {
            globalExcludedRevprop = fixEmptyAndTrim(
                    req.getParameter("svn.global_excluded_revprop"));

            // Save configuration
            save();

            return super.configure(req);
        }

        /**
         * Creates {@link ISVNAuthenticationProvider} backed by {@link #credentials}.
         * This method must be invoked on the master, but the returned object is remotable.
         *
         * <p>
         * Therefore, to access {@link ISVNAuthenticationProvider}, you need to call this method
         * on the master, then pass the object to the slave side, then call
         * {@link SubversionSCM#createSvnClientManager(ISVNAuthenticationProvider)} on the slave.
         *
         * @see SubversionSCM#createSvnClientManager(ISVNAuthenticationProvider)
         */
        public ISVNAuthenticationProvider createAuthenticationProvider() {
            return new SVNAuthenticationProviderImpl(remotableProvider);
        }

        /**
         * Submits the authentication info.
         */
        // TODO: stapler should do multipart/form-data handling 
        public void doPostCredential(StaplerRequest req, StaplerResponse rsp) throws IOException, ServletException {
            Hudson.getInstance().checkPermission(Hudson.ADMINISTER);

            MultipartFormDataParser parser = new MultipartFormDataParser(req);

            CrumbIssuer crumbIssuer = Hudson.getInstance().getCrumbIssuer();
            if (crumbIssuer!=null && !crumbIssuer.validateCrumb(req, parser)) {
                rsp.sendError(HttpServletResponse.SC_FORBIDDEN,"No crumb found");
                return;
            }
            
            String url = parser.get("url");

            String kind = parser.get("kind");
            int idx = Arrays.asList("","password","publickey","certificate").indexOf(kind);

            final String username = parser.get("username"+idx);
            final String password = parser.get("password"+idx);


            // SVNKit wants a key in a file
            final File keyFile;
            FileItem item=null;
            if(idx <= 1) {
                keyFile = null;
            } else {
                item = parser.getFileItem(kind.equals("publickey")?"privateKey":"certificate");
                keyFile = File.createTempFile("hudson","key");
                if(item!=null) {
                    try {
                        item.write(keyFile);
                    } catch (Exception e) {
                        throw new IOException2(e);
                    }
                    if(PuTTYKey.isPuTTYKeyFile(keyFile)) {
                        // TODO: we need a passphrase support
                        LOGGER.info("Converting "+keyFile+" from PuTTY format to OpenSSH format");
                        new PuTTYKey(keyFile,null).toOpenSSH(keyFile);
                    }
                }
            }

            // we'll record what credential we are trying here.
            StringWriter log = new StringWriter();
            final PrintWriter logWriter = new PrintWriter(log);

            try {
                postCredential(url, username, password, keyFile, logWriter);
                rsp.sendRedirect("credentialOK");
            } catch (SVNException e) {
                logWriter.println("FAILED: "+e.getErrorMessage());
                req.setAttribute("message",log.toString());
                req.setAttribute("pre",true);
                req.setAttribute("exception",e);
                rsp.forward(Hudson.getInstance(),"error",req);
            } finally {
                if(keyFile!=null)
                    keyFile.delete();
                if(item!=null)
                    item.delete();
            }
        }

        /**
         * Submits the authentication info.
         *
         * This code is fairly ugly because of the way SVNKit handles credentials.
         */
        public void postCredential(String url, final String username, final String password, final File keyFile, final PrintWriter logWriter) throws SVNException, IOException {
            SVNRepository repository = null;

            try {
                final boolean[] authenticationAttemped = new boolean[1];
                final boolean[] authenticationAcknowled = new boolean[1];

                // the way it works with SVNKit is that
                // 1) svnkit calls AuthenticationManager asking for a credential.
                //    this is when we can see the 'realm', which identifies the user domain.
                // 2) DefaultSVNAuthenticationManager returns the username and password we set below
                // 3) if the authentication is successful, svnkit calls back acknowledgeAuthentication
                //    (so we store the password info here)
                repository = SVNRepositoryFactory.create(SVNURL.parseURIDecoded(url));
                repository.setTunnelProvider(SVNWCUtil.createDefaultOptions(true));
                repository.setAuthenticationManager(new DefaultSVNAuthenticationManager(SVNWCUtil.getDefaultConfigurationDirectory(), true, username, password, keyFile, password) {
                    Credential cred = null;

                    @Override
                    public SVNAuthentication getFirstAuthentication(String kind, String realm, SVNURL url) throws SVNException {
                        authenticationAttemped[0] = true;
                        if (kind.equals(ISVNAuthenticationManager.USERNAME))
                            // when using svn+ssh, svnkit first asks for ISVNAuthenticationManager.SSH
                            // authentication to connect via SSH, then calls this method one more time
                            // to get the user name. Perhaps svn takes user name on its own, separate
                            // from OS user name? In any case, we need to return the same user name.
                            // I don't set the cred field here, so that the 1st credential for ssh
                            // won't get clobbered.
                            return new SVNUserNameAuthentication(username, false);
                        if (kind.equals(ISVNAuthenticationManager.PASSWORD)) {
                            logWriter.println("Passing user name " + username + " and password you entered");
                            cred = new PasswordCredential(username, password);
                        }
                        if (kind.equals(ISVNAuthenticationManager.SSH)) {
                            if (keyFile == null) {
                                logWriter.println("Passing user name " + username + " and password you entered to SSH");
                                cred = new PasswordCredential(username, password);
                            } else {
                                logWriter.println("Attempting a public key authentication with username " + username);
                                cred = new SshPublicKeyCredential(username, password, keyFile);
                            }
                        }
                        if (kind.equals(ISVNAuthenticationManager.SSL)) {
                            logWriter.println("Attempting an SSL client certificate authentcation");
                            cred = new SslClientCertificateCredential(keyFile, password);
                        }

                        if (cred == null) {
                            logWriter.println("Unknown authentication method: " + kind);
                            return null;
                        }
                        return cred.createSVNAuthentication(kind);
                    }

                    /**
                     * Getting here means the authentication tried in {@link #getFirstAuthentication(String, String, SVNURL)}
                     * didn't work.
                     */
                    @Override
                    public SVNAuthentication getNextAuthentication(String kind, String realm, SVNURL url) throws SVNException {
                        SVNErrorManager.authenticationFailed("Authentication failed for " + url, null);
                        return null;
                    }

                    @Override
                    public void acknowledgeAuthentication(boolean accepted, String kind, String realm, SVNErrorMessage errorMessage, SVNAuthentication authentication) throws SVNException {
                        authenticationAcknowled[0] = true;
                        if (accepted) {
                            assert cred != null;
                            credentials.put(realm, cred);
                            save();
                        } else {
                            logWriter.println("Failed to authenticate: " + errorMessage);
                            if (errorMessage.getCause() != null)
                                errorMessage.getCause().printStackTrace(logWriter);
                        }
                        super.acknowledgeAuthentication(accepted, kind, realm, errorMessage, authentication);
                    }
                });
                repository.testConnection();

                if(!authenticationAttemped[0]) {
                    logWriter.println("No authentication was attemped.");
                    throw new SVNCancelException();
                }
                if (!authenticationAcknowled[0]) {
                    logWriter.println("Authentication was not acknowledged.");
                    throw new SVNCancelException();
                }
            } finally {
                if (repository != null)
                    repository.closeSession();
            }
        }

        /**
         * validate the value for a remote (repository) location.
         */
        public FormValidation doCheckRemote(StaplerRequest req, @QueryParameter String value) {
            // syntax check first
            String url = Util.nullify(value);
            if (url == null)
                return FormValidation.ok();

            // remove unneeded whitespaces
            url = url.trim();
            if(!URL_PATTERN.matcher(url).matches())
                return FormValidation.errorWithMarkup("Invalid URL syntax. See "
                    + "<a href=\"http://svnbook.red-bean.com/en/1.2/svn-book.html#svn.basic.in-action.wc.tbl-1\">this</a> "
                    + "for information about valid URLs.");

            // Test the connection only if we have admin permission
            if (!Hudson.getInstance().hasPermission(Hudson.ADMINISTER))
                return FormValidation.ok();

            try {
                SVNURL repoURL = SVNURL.parseURIDecoded(url);
                if (checkRepositoryPath(repoURL)!=SVNNodeKind.NONE)
                    // something exists
                    return FormValidation.ok();

                SVNRepository repository = null;
                try {
                    repository = getRepository(repoURL);
                    long rev = repository.getLatestRevision();
                    // now go back the tree and find if there's anything that exists
                    String repoPath = getRelativePath(repoURL, repository);
                    String p = repoPath;
                    while(p.length()>0) {
                        p = SVNPathUtil.removeTail(p);
                        if(repository.checkPath(p,rev)==SVNNodeKind.DIR) {
                            // found a matching path
                            List<SVNDirEntry> entries = new ArrayList<SVNDirEntry>();
                            repository.getDir(p,rev,false,entries);

                            // build up the name list
                            List<String> paths = new ArrayList<String>();
                            for (SVNDirEntry e : entries)
                                if(e.getKind()==SVNNodeKind.DIR)
                                    paths.add(e.getName());

                            String head = SVNPathUtil.head(repoPath.substring(p.length() + 1));
                            String candidate = EditDistance.findNearest(head,paths);

                            return FormValidation.error("'%1$s/%2$s' doesn't exist in the repository. Maybe you meant '%1$s/%3$s'?",
                                    p, head, candidate);
                        }
                    }

                    return FormValidation.error(repoPath+" doesn't exist in the repository");
                } finally {
                    if (repository != null)
                        repository.closeSession();
                }
            } catch (SVNException e) {
                String message="";
                message += "Unable to access "+Util.escape(url)+" : "+Util.escape( e.getErrorMessage().getFullMessage());
                message += " <a href='#' id=svnerrorlink onclick='javascript:" +
                    "document.getElementById(\"svnerror\").style.display=\"block\";" +
                    "document.getElementById(\"svnerrorlink\").style.display=\"none\";" +
                    "return false;'>(show details)</a>";
                message += "<pre id=svnerror style='display:none'>"+Functions.printThrowable(e)+"</pre>";
                message += " (Maybe you need to <a target='_new' href='"+req.getContextPath()+"/scm/SubversionSCM/enterCredential?"+url+"'>enter credential</a>?)";
                message += "<br>";
                LOGGER.log(Level.INFO, "Failed to access subversion repository "+url,e);
                return FormValidation.errorWithMarkup(message);
            }
        }

        public SVNNodeKind checkRepositoryPath(SVNURL repoURL) throws SVNException {
            SVNRepository repository = null;

            try {
                repository = getRepository(repoURL);
                repository.testConnection();

                long rev = repository.getLatestRevision();
                String repoPath = getRelativePath(repoURL, repository);
                return repository.checkPath(repoPath, rev);
            } finally {
                if (repository != null)
                    repository.closeSession();
            }
        }

        protected SVNRepository getRepository(SVNURL repoURL) throws SVNException {
            SVNRepository repository = SVNRepositoryFactory.create(repoURL);

            ISVNAuthenticationManager sam = SVNWCUtil.createDefaultAuthenticationManager();
            sam = new FilterSVNAuthenticationManager(sam) {
                // If there's no time out, the blocking read operation may hang forever, because TCP itself
                // has no timeout. So always use some time out. If the underlying implementation gives us some
                // value (which may come from ~/.subversion), honor that, as long as it sets some timeout value.
                @Override
                public int getReadTimeout(SVNRepository repository) {
                    int r = super.getReadTimeout(repository);
                    if(r<=0)    r = DEFAULT_TIMEOUT;
                    return r;
                }
            };
            sam.setAuthenticationProvider(createAuthenticationProvider());
            repository.setAuthenticationManager(sam);

            return repository;
        }
        
        public static String getRelativePath(SVNURL repoURL, SVNRepository repository) throws SVNException {
            String repoPath = repoURL.getPath().substring(repository.getRepositoryRoot(false).getPath().length());
            if(!repoPath.startsWith("/"))    repoPath="/"+repoPath;
            return repoPath;
        }

        /**
         * validate the value for a local location (local checkout directory).
         */
        public FormValidation doCheckLocal(@QueryParameter String value) throws IOException, ServletException {
            String v = Util.nullify(value);
            if (v == null)
                // local directory is optional so this is ok
                return FormValidation.ok();

            v = v.trim();

            // check if a absolute path has been supplied
            // (the last check with the regex will match windows drives)
            if (v.startsWith("/") || v.startsWith("\\") || v.startsWith("..") || v.matches("^[A-Za-z]:"))
                return FormValidation.error("absolute path is not allowed");

            // all tests passed so far
            return FormValidation.ok();
        }

        /**
         * Validates the excludeRegions Regex
         */
        public FormValidation doCheckExcludedRegions(@QueryParameter String value) throws IOException, ServletException {
            for (String region : Util.fixNull(value).trim().split("[\\r\\n]+"))
                try {
                    Pattern.compile(region);
                } catch (PatternSyntaxException e) {
                    return FormValidation.error("Invalid regular expression. " + e.getMessage());
                }
            return FormValidation.ok();
        }

        private static final Pattern USERNAME_PATTERN = Pattern.compile("\\w+");

        /**
         * Validates the excludeUsers field
         */
        public FormValidation doCheckExcludedUsers(@QueryParameter String value) throws IOException, ServletException {
            for (String user : Util.fixNull(value).trim().split("[\\r\\n]+")) {
                user = user.trim();

                if ("".equals(user)) {
                    continue;
                }

                if (!USERNAME_PATTERN.matcher(user).matches()) {
                    return FormValidation.error("Invalid username: " + user);
                }
            }

            return FormValidation.ok();
        }

        /**
         * Validates the excludeCommitMessages field
         */
        public FormValidation doCheckExcludedCommitMessages(@QueryParameter String value) throws IOException, ServletException {
            for (String message : Util.fixNull(value).trim().split("[\\r\\n]+")) {
                try {
                    Pattern.compile(message);
                } catch (PatternSyntaxException e) {
                    return FormValidation.error("Invalid regular expression. " + e.getMessage());
                }
            }
            return FormValidation.ok();
        }

        /**
         * Validates the remote server supports custom revision properties
         */
        public FormValidation doCheckRevisionPropertiesSupported(@QueryParameter String value) throws IOException, ServletException {
            String v = Util.fixNull(value).trim();
            if (v.length() == 0)
                return FormValidation.ok();

            // Test the connection only if we have admin permission
            if (!Hudson.getInstance().hasPermission(Hudson.ADMINISTER))
                return FormValidation.ok();

            try {
                SVNURL repoURL = SVNURL.parseURIDecoded(v);
                if (checkRepositoryPath(repoURL)!=SVNNodeKind.NONE)
                    // something exists
                    return FormValidation.ok();

                SVNRepository repository = null;
                try {
                    repository = getRepository(repoURL);
                    if (repository.hasCapability(SVNCapability.LOG_REVPROPS))
                        return FormValidation.ok();
                } finally {
                    if (repository != null)
                        repository.closeSession();
                }
            } catch (SVNException e) {
                String message="";
                message += "Unable to access "+Util.escape(v)+" : "+Util.escape( e.getErrorMessage().getFullMessage());
                LOGGER.log(Level.INFO, "Failed to access subversion repository "+v,e);
                return FormValidation.errorWithMarkup(message);
            }

            return FormValidation.warning(Messages.SubversionSCM_excludedRevprop_notSupported(v));
        }
        
        static {
            new Initializer();
        }
    }

    public boolean repositoryLocationsNoLongerExist(AbstractBuild<?,?> build, TaskListener listener) {
        PrintStream out = listener.getLogger();

        for (ModuleLocation l : getLocations(build))
            try {
                if (getDescriptor().checkRepositoryPath(l.getSVNURL()) == SVNNodeKind.NONE) {
                    out.println("Location '" + l.remote + "' does not exist");

                    ParametersAction params = build.getAction(ParametersAction.class);
                    if (params != null) {
                        // since this is used to disable projects, be conservative
                        LOGGER.fine("Location could be expanded on build '" + build
                                + "' parameters values:");
                        return false;
                    }
                    return true;
                }
            } catch (SVNException e) {
                // be conservative, since we are just trying to be helpful in detecting
                // non existent locations. If we can't detect that, we'll do nothing
                LOGGER.log(FINE, "Location check failed",e);
            }
        return false;
    }

    static final Pattern URL_PATTERN = Pattern.compile("(https?|svn(\\+[a-z0-9]+)?|file)://.+");

    private static final long serialVersionUID = 1L;

    // noop, but this forces the initializer to run.
    public static void init() {}

    static {
        new Initializer();
    }

    private static final class Initializer {
        static {
            if(Boolean.getBoolean("hudson.spool-svn"))
                DAVRepositoryFactory.setup(new DefaultHTTPConnectionFactory(null,true,null));
            else
                DAVRepositoryFactory.setup();   // http, https
            SVNRepositoryFactoryImpl.setup();   // svn, svn+xxx
            FSRepositoryFactory.setup();    // file

            // disable the connection pooling, which causes problems like
            // http://www.nabble.com/SSH-connection-problems-p12028339.html
            if(System.getProperty("svnkit.ssh2.persistent")==null)
                System.setProperty("svnkit.ssh2.persistent","false");

            // use SVN1.4 compatible workspace by default.
            SVNAdminAreaFactory.setSelector(new SubversionWorkspaceSelector());
        }
    }

    /**
     * small structure to store local and remote (repository) location
     * information of the repository. As a addition it holds the invalid field
     * to make failure messages when doing a checkout possible
     */
    public static final class ModuleLocation implements Serializable {
        /**
         * Subversion URL to check out.
         *
         * This may include "@NNN" at the end to indicate a fixed revision.
         */
        public final String remote;
        /**
         * Remembers the user-given value.
         * Can be null.
         *
         * @deprecated
         *      Code should use {@link #getLocalDir()}. This field is only intended for form binding.
         */
        public final String local;

        /**
         * Cache of the repository UUID.
         */
        private transient volatile UUID repositoryUUID;
        private transient volatile SVNURL repositoryRoot;

        @DataBoundConstructor
        public ModuleLocation(String remote, String local) {
            this.remote = Util.removeTrailingSlash(Util.fixNull(remote).trim());
            this.local = fixEmptyAndTrim(local);
        }

        /**
         * Local directory to place the file to.
         * Relative to the workspace root.
         */
        public String getLocalDir() {
            if(local==null)
                return getLastPathComponent(remote);
            return local;
        }

        /**
         * Returns the pure URL portion of {@link #remote} by removing
         * possible "@NNN" suffix.
         */
        public String getURL() {
            int idx = remote.lastIndexOf('@');
            if(idx>0) {
                try {
                    String n = remote.substring(idx+1);
                    Long.parseLong(n);
                    return remote.substring(0,idx);
                } catch (NumberFormatException e) {
                    // not a revision number
                }
            }
            return remote;
        }

        /**
         * Gets {@link #remote} as {@link SVNURL}.
         */
        public SVNURL getSVNURL() throws SVNException {
            return SVNURL.parseURIEncoded(getURL());
        }

        /**
         * Repository UUID. Lazy computed and cached.
         */
        public UUID getUUID() throws SVNException {
            if(repositoryUUID==null || repositoryRoot==null) {
                synchronized (this) {
                    SVNRepository r = openRepository();
                    r.testConnection(); // make sure values are fetched
                    repositoryUUID = UUID.fromString(r.getRepositoryUUID(false));
                    repositoryRoot = r.getRepositoryRoot(false);
                }
            }
            return repositoryUUID;
        }

        public SVNRepository openRepository() throws SVNException {
            return Hudson.getInstance().getDescriptorByType(DescriptorImpl.class).getRepository(getSVNURL());
        }

        public SVNURL getRepositoryRoot() throws SVNException {
            getUUID();
            return repositoryRoot;
        }

        /**
         * Figures out which revision to check out.
         *
         * If {@link #remote} is {@code url@rev}, then this method
         * returns that specific revision.
         *
         * @param defaultValue
         *      If "@NNN" portion is not in the URL, this value will be returned.
         *      Normally, this is the SVN revision timestamped at the build date.
         */
        public SVNRevision getRevision(SVNRevision defaultValue) {
            int idx = remote.lastIndexOf('@');
            if(idx>0) {
                try {
                    String n = remote.substring(idx+1);
                    return SVNRevision.create(Long.parseLong(n));
                } catch (NumberFormatException e) {
                    // not a revision number
                }
            }
            return defaultValue;
        }

        private String getExpandedRemote(AbstractBuild<?,?> build) {
            String outRemote = remote;

            ParametersAction parameters = build.getAction(ParametersAction.class);
            if (parameters != null)
                outRemote = parameters.substitute(build, remote);

            return outRemote;
        }

        /**
         * Expand location value based on Build parametric execution.
         *
         * @param build
         *            Build instance for expanding parameters into their values
         *
         * @return Output ModuleLocation expanded according to Build parameters
         *         values.
         */
        public ModuleLocation getExpandedLocation(AbstractBuild<?, ?> build) {
            return new ModuleLocation(getExpandedRemote(build), getLocalDir());
        }
        
        public String toString() {
            return remote;
        }

        private static final long serialVersionUID = 1L;

        public static List<ModuleLocation> parse(String[] remoteLocations, String[] localLocations) {
            List<ModuleLocation> modules = new ArrayList<ModuleLocation>();
            if (remoteLocations != null && localLocations != null) {
                int entries = Math.min(remoteLocations.length, localLocations.length);

                for (int i = 0; i < entries; i++) {
                    // the remote (repository) location
                    String remoteLoc = Util.nullify(remoteLocations[i]);

                    if (remoteLoc != null) {// null if skipped
                        remoteLoc = Util.removeTrailingSlash(remoteLoc.trim());
                        modules.add(new ModuleLocation(remoteLoc, Util.nullify(localLocations[i])));
                    }
                }
            }
            return modules;
        }
    }

    private static final Logger LOGGER = Logger.getLogger(SubversionSCM.class.getName());

    /**
     * Network timeout in milliseconds.
     * The main point of this is to prevent infinite hang, so it should be a rather long value to avoid
     * accidental time out problem.
     */
    public static int DEFAULT_TIMEOUT = Integer.getInteger(SubversionSCM.class.getName()+".timeout",3600*1000);

    /**
     * Enables trace logging of Ganymed SSH library.
     * <p>
     * Intended to be invoked from Groovy console.
     */
    public static void enableSshDebug(Level level) {
        if(level==null)     level= Level.FINEST; // default

        final Level lv = level;

        com.trilead.ssh2.log.Logger.enabled=true;
        com.trilead.ssh2.log.Logger.logger = new DebugLogger() {
            private final Logger LOGGER = Logger.getLogger(SCPClient.class.getPackage().getName());
            public void log(int level, String className, String message) {
                LOGGER.log(lv,className+' '+message);
            }
        };
    }

    /*package*/ static boolean compareSVNAuthentications(SVNAuthentication a1, SVNAuthentication a2) {
        if (a1==null && a2==null)       return true;
        if (a1==null || a2==null)       return false;
        if (a1.getClass()!=a2.getClass())    return false;

        try {
            return describeBean(a1).equals(describeBean(a2));
        } catch (IllegalAccessException e) {
            return false;
        } catch (InvocationTargetException e) {
            return false;
        } catch (NoSuchMethodException e) {
            return false;
        }
    }

    /**
     * In preparation for a comparison, char[] needs to be converted that supports value equality.
     */
    private static Map describeBean(Object o) throws InvocationTargetException, NoSuchMethodException, IllegalAccessException {
        Map<?,?> m = PropertyUtils.describe(o);
        for (Entry e : m.entrySet()) {
            Object v = e.getValue();
            if (v instanceof char[]) {
                char[] chars = (char[]) v;
                e.setValue(new String(chars));
            }
        }
        return m;
    }
}
