/*
 * Copyright 2005-2008 Noelios Consulting.
 * 
 * The contents of this file are subject to the terms of the Common Development
 * and Distribution License (the "License"). You may not use this file except in
 * compliance with the License.
 * 
 * You can obtain a copy of the license at
 * http://www.opensource.org/licenses/cddl1.txt See the License for the specific
 * language governing permissions and limitations under the License.
 * 
 * When distributing Covered Code, include this CDDL HEADER in each file and
 * include the License file at http://www.opensource.org/licenses/cddl1.txt If
 * applicable, add the following below this CDDL HEADER, with the fields
 * enclosed by brackets "[]" replaced with your own identifying information:
 * Portions Copyright [yyyy] [name of copyright owner]
 */

package com.noelios.restlet;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLStreamHandler;
import java.net.URLStreamHandlerFactory;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Enumeration;
import java.util.Iterator;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.restlet.Application;
import org.restlet.Client;
import org.restlet.Component;
import org.restlet.Context;
import org.restlet.Directory;
import org.restlet.Guard;
import org.restlet.Server;
import org.restlet.data.ChallengeScheme;
import org.restlet.data.CharacterSet;
import org.restlet.data.ClientInfo;
import org.restlet.data.Cookie;
import org.restlet.data.CookieSetting;
import org.restlet.data.Dimension;
import org.restlet.data.Form;
import org.restlet.data.Language;
import org.restlet.data.MediaType;
import org.restlet.data.Parameter;
import org.restlet.data.Preference;
import org.restlet.data.Product;
import org.restlet.data.Protocol;
import org.restlet.data.Request;
import org.restlet.data.Response;
import org.restlet.resource.Representation;
import org.restlet.resource.Resource;
import org.restlet.resource.Variant;
import org.restlet.util.Series;

import com.noelios.restlet.application.ApplicationHelper;
import com.noelios.restlet.authentication.AuthenticationHelper;
import com.noelios.restlet.authentication.AuthenticationUtils;
import com.noelios.restlet.authentication.HttpAmazonS3Helper;
import com.noelios.restlet.authentication.HttpBasicHelper;
import com.noelios.restlet.authentication.HttpDigestHelper;
import com.noelios.restlet.authentication.SmtpPlainHelper;
import com.noelios.restlet.component.ComponentHelper;
import com.noelios.restlet.http.ContentType;
import com.noelios.restlet.http.HttpClientCall;
import com.noelios.restlet.http.HttpClientConverter;
import com.noelios.restlet.http.HttpServerConverter;
import com.noelios.restlet.http.StreamClientHelper;
import com.noelios.restlet.http.StreamServerHelper;
import com.noelios.restlet.local.ClapClientHelper;
import com.noelios.restlet.local.DirectoryResource;
import com.noelios.restlet.local.FileClientHelper;
import com.noelios.restlet.util.CookieReader;
import com.noelios.restlet.util.CookieUtils;
import com.noelios.restlet.util.FormUtils;
import com.noelios.restlet.util.SecurityUtils;

/**
 * Restlet factory supported by the engine.
 * 
 * @author Jerome Louvel (contact@noelios.com)
 */
public class Engine extends org.restlet.util.Engine {
    /** Obtain a suitable logger. */
    private static Logger logger = Logger.getLogger(Engine.class
            .getCanonicalName());

    /** Complete version. */
    @SuppressWarnings("hiding")
    public static final String VERSION = org.restlet.util.Engine.VERSION;

    /** Complete version header. */
    public static final String VERSION_HEADER = "Noelios-Restlet-Engine/"
            + VERSION;

    /**
     * Returns the registered Noelios Restlet engine.
     * 
     * @return The registered Noelios Restlet engine.
     */
    public static Engine getInstance() {
        return (Engine) org.restlet.util.Engine.getInstance();
    }

    /**
     * Parses the "java.version" system property and returns the first digit of
     * the version number of the Java Runtime Environment (e.g. "1" for
     * "1.3.0").
     * 
     * @see <a href="http://java.sun.com/j2se/versioning_naming.html">Official
     *      Java versioning</a>
     * @return The major version number of the Java Runtime Environment.
     */
    public static int getJavaMajorVersion() {
        int result;
        String javaVersion = System.getProperty("java.version");
        try {
            result = Integer.parseInt(javaVersion.substring(0, javaVersion
                    .indexOf(".")));
        } catch (Exception e) {
            result = 0;
        }

        return result;
    }

    /**
     * Parses the "java.version" system property and returns the second digit of
     * the version number of the Java Runtime Environment (e.g. "3" for
     * "1.3.0").
     * 
     * @see <a href="http://java.sun.com/j2se/versioning_naming.html">Official
     *      Java versioning</a>
     * @return The minor version number of the Java Runtime Environment.
     */
    public static int getJavaMinorVersion() {
        int result;
        String javaVersion = System.getProperty("java.version");
        try {
            result = Integer.parseInt(javaVersion.split("\\.")[1]);
        } catch (Exception e) {
            result = 0;
        }

        return result;
    }

    /**
     * Parses the "java.version" system property and returns the update release
     * number of the Java Runtime Environment (e.g. "10" for "1.3.0_10").
     * 
     * @see <a href="http://java.sun.com/j2se/versioning_naming.html">Official
     *      Java versioning</a>
     * @return The release number of the Java Runtime Environment or 0 if it
     *         does not exist.
     */
    public static int getJavaUpdateVersion() {
        int result;
        String javaVersion = System.getProperty("java.version");
        try {
            result = Integer.parseInt(javaVersion.substring(javaVersion
                    .indexOf('_') + 1));
        } catch (Exception e) {
            result = 0;
        }

        return result;
    }

    /**
     * Registers a new Noelios Restlet Engine.
     * 
     * @return The registered engine.
     */
    public static Engine register() {
        return register(true);
    }

    /**
     * Registers a new Noelios Restlet Engine.
     * 
     * @param discoverConnectors
     *                True if connectors should be automatically discovered.
     * @return The registered engine.
     */
    public static Engine register(boolean discoverConnectors) {
        Engine result = new Engine(discoverConnectors);
        org.restlet.util.Engine.setInstance(result);
        return result;
    }

    /** List of available authentication helpers. */
    private volatile List<AuthenticationHelper> registeredAuthentications;

    /** List of available client connectors. */
    private volatile List<ClientHelper> registeredClients;

    /** List of available server connectors. */
    private volatile List<ServerHelper> registeredServers;

    /**
     * Constructor that will automatically attempt to discover connectors.
     */
    public Engine() {
        this(true);
    }

    /**
     * Constructor.
     * 
     * @param discoverHelpers
     *                True if helpers should be automatically discovered.
     */
    public Engine(boolean discoverHelpers) {
        this.registeredClients = new CopyOnWriteArrayList<ClientHelper>();
        this.registeredServers = new CopyOnWriteArrayList<ServerHelper>();
        this.registeredAuthentications = new CopyOnWriteArrayList<AuthenticationHelper>();

        if (discoverHelpers) {
            discoverConnectors();
            discoverAuthentications();
        }
    }

    @Override
    public int authenticate(Request request, Guard guard) {
        return AuthenticationUtils.authenticate(request, guard);
    }

    @Override
    public void challenge(Response response, boolean stale, Guard guard) {
        AuthenticationUtils.challenge(response, stale, guard);
    }

    /**
     * Copies the given header parameters into the given {@link Response}.
     * 
     * @param responseHeaders
     *                The headers to copy.
     * @param response
     *                The response to update. Must contain a
     *                {@link Representation} to copy the representation headers
     *                in it.
     * @param logger
     *                The logger to use.
     * @see org.restlet.util.Engine#copyResponseHeaders(java.lang.Iterable,
     *      org.restlet.data.Response, java.util.logging.Logger)
     */
    @Override
    public void copyResponseHeaders(Iterable<Parameter> responseHeaders,
            Response response, Logger logger) {
        HttpClientConverter.copyResponseTransportHeaders(responseHeaders,
                response, logger);
        HttpClientCall.copyResponseEntityHeaders(responseHeaders, response
                .getEntity());
    }

    /**
     * Copies the headers of the given {@link Response} into the given
     * {@link Series}.
     * 
     * @param response
     *                The response to update. Should contain a
     *                {@link Representation} to copy the representation headers
     *                from it.
     * @param headers
     *                The Series to copy the headers in.
     * @param logger
     *                The logger to use.
     * @see org.restlet.util.Engine#copyResponseHeaders(Response, Series,
     *      Logger)
     */
    @Override
    public void copyResponseHeaders(Response response,
            Series<Parameter> headers, Logger logger) {
        HttpServerConverter.addResponseHeaders(response, headers);
        HttpServerConverter.addEntityHeaders(response.getEntity(), headers);
    }

    @Override
    public Resource createDirectoryResource(Directory handler, Request request,
            Response response) throws IOException {
        return new DirectoryResource(handler, request, response);
    }

    @Override
    public ApplicationHelper createHelper(Application application,
            Context parentContext) {
        return new ApplicationHelper(application, parentContext);
    }

    @Override
    public ClientHelper createHelper(Client client, String helperClass) {
        ClientHelper result = null;

        if (client.getProtocols().size() > 0) {
            ClientHelper connector = null;
            for (Iterator<ClientHelper> iter = getRegisteredClients()
                    .iterator(); (result == null) && iter.hasNext();) {
                connector = iter.next();

                if (connector.getProtocols().containsAll(client.getProtocols())) {
                    if ((helperClass == null)
                            || connector.getClass().getCanonicalName().equals(
                                    helperClass)) {
                        try {
                            result = connector.getClass().getConstructor(
                                    Client.class).newInstance(client);
                        } catch (Exception e) {
                            logger
                                    .log(
                                            Level.SEVERE,
                                            "Exception while instantiation the client connector.",
                                            e);
                        }
                    }
                }
            }

            if (result == null) {
                // Couldn't find a matching connector
                StringBuilder sb = new StringBuilder();
                sb
                        .append("No available client connector supports the required protocols: ");

                for (Protocol p : client.getProtocols()) {
                    sb.append("'").append(p.getName()).append("' ");
                }

                sb
                        .append(". Please add the JAR of a matching connector to your classpath.");

                logger.log(Level.WARNING, sb.toString());
            }
        }

        return result;
    }

    @Override
    public ComponentHelper createHelper(Component component) {
        return new ComponentHelper(component);
    }

    @Override
    public ServerHelper createHelper(Server server, String helperClass) {
        ServerHelper result = null;

        if (server.getProtocols().size() > 0) {
            ServerHelper connector = null;
            for (Iterator<ServerHelper> iter = getRegisteredServers()
                    .iterator(); (result == null) && iter.hasNext();) {
                connector = iter.next();

                if ((helperClass == null)
                        || connector.getClass().getCanonicalName().equals(
                                helperClass)) {
                    if (connector.getProtocols().containsAll(
                            server.getProtocols())) {
                        try {
                            result = connector.getClass().getConstructor(
                                    Server.class).newInstance(server);
                        } catch (Exception e) {
                            logger
                                    .log(
                                            Level.SEVERE,
                                            "Exception while instantiation the server connector.",
                                            e);
                        }
                    }
                }
            }

            if (result == null) {
                // Couldn't find a matching connector
                StringBuilder sb = new StringBuilder();
                sb
                        .append("No available server connector supports the required protocols: ");

                for (Protocol p : server.getProtocols()) {
                    sb.append("'").append(p.getName()).append("' ");
                }

                sb
                        .append(". Please add the JAR of a matching connector to your classpath.");

                logger.log(Level.WARNING, sb.toString());
            }
        }

        return result;
    }

    /**
     * Discovers the authentication helpers and register the default helpers.
     */
    private void discoverAuthentications() {
        // Find the factory class name
        ClassLoader classLoader = org.restlet.util.Engine.getClassLoader();

        discoverHelpers(classLoader,
                "META-INF/services/com.noelios.restlet.AuthenticationHelper",
                getRegisteredAuthentications(), null);

        // Register the default helpers that will be used if no
        // other helper has been found
        registerDefaultAuthentications();
    }

    /**
     * Discovers client connectors in the classpath.
     * 
     * @param classLoader
     *                Classloader to search.
     */
    private void discoverClientConnectors(ClassLoader classLoader) {
        discoverHelpers(classLoader,
                "META-INF/services/com.noelios.restlet.ClientHelper",
                getRegisteredClients(), Client.class);
    }

    /**
     * Discovers the server and client connectors and register the default
     * connectors.
     */
    private void discoverConnectors() {
        // Find the factory class name
        ClassLoader classLoader = org.restlet.util.Engine.getClassLoader();

        // Register the client connector providers
        discoverClientConnectors(classLoader);

        // Register the server connector providers
        discoverServerConnectors(classLoader);

        // Register the default connectors that will be used if no
        // other connector has been found
        registerDefaultConnectors();
    }

    /**
     * Looks for pluggable helpers in the classpath and add them to the current
     * list.
     * 
     * @param classLoader
     *                Classloader to search.
     * @param descriptor
     *                The descriptor location to parse.
     * @param helpers
     *                The list of helpers to update.
     * @param constructorClass
     *                The constructor parameter class to look for.
     */
    @SuppressWarnings("unchecked")
    private void discoverHelpers(ClassLoader classLoader, String descriptor,
            List helpers, Class constructorClass) {
        try {
            for (Enumeration<URL> configUrls = classLoader
                    .getResources(descriptor); configUrls.hasMoreElements();) {
                URL configURL = configUrls.nextElement();

                BufferedReader reader = null;
                try {
                    reader = new BufferedReader(new InputStreamReader(configURL
                            .openStream(), "utf-8"));
                    String line = reader.readLine();

                    while (line != null) {
                        String provider = getProviderClassName(line);

                        if ((provider != null) && (!provider.equals(""))) {
                            // Instantiate the factory
                            try {
                                Class providerClass = Class.forName(provider);

                                if (constructorClass == null) {
                                    helpers.add(providerClass.newInstance());
                                } else {
                                    helpers.add(providerClass.getConstructor(
                                            constructorClass).newInstance(
                                            constructorClass.cast(null)));
                                }
                            } catch (Exception e) {
                                logger.log(Level.SEVERE,
                                        "Unable to register the connector "
                                                + provider, e);
                            }
                        }

                        line = reader.readLine();
                    }
                } catch (IOException e) {
                    logger.log(Level.SEVERE,
                            "Unable to read the provider descriptor: "
                                    + configURL.toString());
                } finally {
                    if (reader != null)
                        reader.close();
                }
            }
        } catch (IOException ioe) {
            logger.log(Level.SEVERE,
                    "Exception while detecting the client connectors.", ioe);
        }
    }

    /**
     * Discovers server connectors in the classpath.
     * 
     * @param classLoader
     *                Classloader to search.
     */
    private void discoverServerConnectors(ClassLoader classLoader) {
        discoverHelpers(classLoader,
                "META-INF/services/com.noelios.restlet.ServerHelper",
                getRegisteredServers(), Server.class);
    }

    /**
     * Finds the authentication helper supporting the given scheme.
     * 
     * @param challengeScheme
     *                The challenge scheme to match.
     * @param clientSide
     *                Indicates if client side support is required.
     * @param serverSide
     *                Indicates if server side support is required.
     * @return The authentication helper or null.
     */
    public AuthenticationHelper findHelper(ChallengeScheme challengeScheme,
            boolean clientSide, boolean serverSide) {
        AuthenticationHelper result = null;
        List<AuthenticationHelper> helpers = getRegisteredAuthentications();
        AuthenticationHelper current;

        for (int i = 0; (result == null) && (i < helpers.size()); i++) {
            current = helpers.get(i);

            if (current.getChallengeScheme().equals(challengeScheme)
                    && ((clientSide && current.isClientSide()) || !clientSide)
                    && ((serverSide && current.isServerSide()) || !serverSide)) {
                result = helpers.get(i);
            }
        }

        return result;
    }

    @Override
    public String formatCookie(Cookie cookie) throws IllegalArgumentException {
        return CookieUtils.format(cookie);
    }

    @Override
    public String formatCookieSetting(CookieSetting cookieSetting)
            throws IllegalArgumentException {
        return CookieUtils.format(cookieSetting);
    }

    @Override
    public String formatDimensions(Collection<Dimension> dimensions) {
        return HttpServerConverter.createVaryHeader(dimensions);
    }

    @Override
    public String formatUserAgent(List<Product> products)
            throws IllegalArgumentException {
        StringBuilder builder = new StringBuilder();

        for (Iterator<Product> iterator = products.iterator(); iterator
                .hasNext();) {
            Product product = iterator.next();
            if (product.getName() == null && product.getName().length() == 0) {
                throw new IllegalArgumentException(
                        "Product name cannot be null.");
            } else {
                builder.append(product.getName());
                if (product.getVersion() != null) {
                    builder.append("/").append(product.getVersion());
                }
                if (product.getComment() != null) {
                    builder.append(" (").append(product.getComment()).append(
                            ")");
                }
            }
            if (iterator.hasNext()) {
                builder.append(" ");
            }
        }

        return builder.toString();
    }

    @Override
    public Variant getPreferredVariant(ClientInfo client,
            List<Variant> variants, Language defaultLanguage) {
        if (variants == null) {
            return null;
        } else {
            List<Language> variantLanguages = null;
            MediaType variantMediaType = null;

            boolean compatibleLanguage = false;
            boolean compatibleMediaType = false;

            Variant currentVariant = null;
            Variant bestVariant = null;

            Preference<Language> currentLanguagePref = null;
            Preference<Language> bestLanguagePref = null;
            Preference<MediaType> currentMediaTypePref = null;
            Preference<MediaType> bestMediaTypePref = null;

            float bestQuality = 0;
            float bestLanguageScore = 0;
            float bestMediaTypeScore = 0;

            // If no language preference is defined or even none matches, we
            // want to make sure that at least a variant can be returned.
            // Based on experience, it appears that browsers are often
            // misconfigured and don't expose all the languages actually
            // understood by end users.
            // Thus, a few other preferences are added to the user's ones:
            // - primary languages inferred from and sorted according to the
            // user's preferences with quality between 0.005 and 0.006
            // - default language (if any) with quality 0.003
            // - primary language of the default language (if available) with
            // quality 0.002
            // - all languages with quality 0.001
            List<Preference<Language>> languagePrefs = client
                    .getAcceptedLanguages();
            List<Preference<Language>> primaryLanguagePrefs = new ArrayList<Preference<Language>>();
            // A default language preference is defined with a better weight
            // than the "All languages" preference
            Preference<Language> defaultLanguagePref = ((defaultLanguage == null) ? null
                    : new Preference<Language>(defaultLanguage, 0.003f));
            Preference<Language> allLanguagesPref = new Preference<Language>(
                    Language.ALL, 0.001f);

            if (languagePrefs.isEmpty()) {
                // All languages accepted.
                languagePrefs.add(new Preference<Language>(Language.ALL));
            } else {
                // Get the primary language preferences that are not currently
                // accepted by the client
                List<String> list = new ArrayList<String>();
                for (Preference<Language> preference : languagePrefs) {
                    Language language = preference.getMetadata();
                    if (!language.getSubTags().isEmpty()) {
                        if (!list.contains(language.getPrimaryTag())) {
                            list.add(language.getPrimaryTag());
                            primaryLanguagePrefs
                                    .add(new Preference<Language>(new Language(
                                            language.getPrimaryTag()),
                                            0.005f + (0.001f * preference
                                                    .getQuality())));
                        }
                    }
                }
                // If the default language is a "primary" language but is not
                // present in the list of all primary languages, add it.
                if (defaultLanguage != null
                        && !defaultLanguage.getSubTags().isEmpty()) {
                    if (!list.contains(defaultLanguage.getPrimaryTag())) {
                        primaryLanguagePrefs.add(new Preference<Language>(
                                new Language(defaultLanguage.getPrimaryTag()),
                                0.002f));
                    }
                }

            }

            // Client preferences are altered
            languagePrefs.addAll(primaryLanguagePrefs);
            if (defaultLanguagePref != null) {
                languagePrefs.add(defaultLanguagePref);
                // In this case, if the client adds the "all languages"
                // preference, the latter is removed, in order to support the
                // default preference defined by the server
                List<Preference<Language>> list = new ArrayList<Preference<Language>>();
                for (Preference<Language> preference : languagePrefs) {
                    Language language = preference.getMetadata();
                    if (!language.equals(Language.ALL)) {
                        list.add(preference);
                    }
                }
                languagePrefs = list;
            }
            languagePrefs.add(allLanguagesPref);

            // For each available variant, we will compute the negotiation score
            // which is dependant on the language score and on the media type
            // score
            for (Iterator<Variant> iter1 = variants.iterator(); iter1.hasNext();) {
                currentVariant = iter1.next();
                variantLanguages = currentVariant.getLanguages();
                variantMediaType = currentVariant.getMediaType();

                // All languages of the current variant are scored.
                for (Language variantLanguage : variantLanguages) {
                    // For each language preference defined in the call
                    // Calculate the score and remember the best scoring
                    // preference
                    for (Iterator<Preference<Language>> iter2 = languagePrefs
                            .iterator(); (variantLanguage != null)
                            && iter2.hasNext();) {
                        currentLanguagePref = iter2.next();
                        float currentScore = getScore(variantLanguage,
                                currentLanguagePref.getMetadata());
                        boolean compatiblePref = (currentScore != -1.0f);
                        // 3) Do we have a better preference?
                        // currentScore *= currentPref.getQuality();
                        if (compatiblePref
                                && ((bestLanguagePref == null) || (currentScore > bestLanguageScore))) {
                            bestLanguagePref = currentLanguagePref;
                            bestLanguageScore = currentScore;
                        }
                    }
                }

                // Are the preferences compatible with the current variant
                // language?
                compatibleLanguage = (variantLanguages.isEmpty())
                        || (bestLanguagePref != null);

                // If no media type preference is defined, assume that all media
                // types are acceptable
                List<Preference<MediaType>> mediaTypePrefs = client
                        .getAcceptedMediaTypes();
                if (mediaTypePrefs.size() == 0)
                    mediaTypePrefs
                            .add(new Preference<MediaType>(MediaType.ALL));

                // For each media range preference defined in the call
                // Calculate the score and remember the best scoring preference
                for (Iterator<Preference<MediaType>> iter2 = mediaTypePrefs
                        .iterator(); compatibleLanguage && iter2.hasNext();) {
                    currentMediaTypePref = iter2.next();
                    float currentScore = getScore(variantMediaType,
                            currentMediaTypePref.getMetadata());
                    boolean compatiblePref = (currentScore != -1.0f);
                    // 3) Do we have a better preference?
                    // currentScore *= currentPref.getQuality();
                    if (compatiblePref
                            && ((bestMediaTypePref == null) || (currentScore > bestMediaTypeScore))) {
                        bestMediaTypePref = currentMediaTypePref;
                        bestMediaTypeScore = currentScore;
                    }

                }

                // Are the preferences compatible with the current media type?
                compatibleMediaType = (variantMediaType == null)
                        || (bestMediaTypePref != null);

                if (compatibleLanguage && compatibleMediaType) {
                    // Do we have a compatible media type?
                    float currentQuality = 0;
                    if (bestLanguagePref != null) {
                        currentQuality += (bestLanguagePref.getQuality() * 10F);
                    } else if (!variantLanguages.isEmpty()) {
                        currentQuality += 0.1F * 10F;
                    }

                    if (bestMediaTypePref != null) {
                        // So, let's conclude on the current variant, its
                        // quality
                        currentQuality += bestMediaTypePref.getQuality();
                    }

                    if (bestVariant == null) {
                        bestVariant = currentVariant;
                        bestQuality = currentQuality;
                    } else if (currentQuality > bestQuality) {
                        bestVariant = currentVariant;
                        bestQuality = currentQuality;
                    }
                }

                // Reset the preference variables
                bestLanguagePref = null;
                bestLanguageScore = 0;
                bestMediaTypePref = null;
                bestMediaTypeScore = 0;
            }

            return bestVariant;
        }
    }

    /**
     * Parses a line to extract the provider class name.
     * 
     * @param line
     *                The line to parse.
     * @return The provider's class name or an empty string.
     */
    private String getProviderClassName(String line) {
        int index = line.indexOf('#');
        if (index != -1)
            line = line.substring(0, index);
        return line.trim();
    }

    /**
     * Returns the list of available authentication helpers.
     * 
     * @return The list of available authentication helpers.
     */
    public List<AuthenticationHelper> getRegisteredAuthentications() {
        return this.registeredAuthentications;
    }

    /**
     * Returns the list of available client connectors.
     * 
     * @return The list of available client connectors.
     */
    public List<ClientHelper> getRegisteredClients() {
        return this.registeredClients;
    }

    /**
     * Returns the list of available server connectors.
     * 
     * @return The list of available server connectors.
     */
    public List<ServerHelper> getRegisteredServers() {
        return this.registeredServers;
    }

    /**
     * Returns a matching score between 2 Languages
     * 
     * @param variantLanguage
     * @param preferenceLanguage
     * @return the positive matching score or -1 if the languages are not
     *         compatible
     */
    private float getScore(Language variantLanguage, Language preferenceLanguage) {
        float score = 0.0f;
        boolean compatibleLang = true;

        // 1) Compare the main tag
        if (variantLanguage.getPrimaryTag().equalsIgnoreCase(
                preferenceLanguage.getPrimaryTag())) {
            score += 100;
        } else if (!preferenceLanguage.getPrimaryTag().equals("*")) {
            compatibleLang = false;
        } else if (!preferenceLanguage.getSubTags().isEmpty()) {
            // Only "*" is an acceptable language range
            compatibleLang = false;
        } else {
            // The valid "*" range has the lowest valid score
            score++;
        }

        if (compatibleLang) {
            // 2) Compare the sub tags
            if ((preferenceLanguage.getSubTags().isEmpty())
                    || (variantLanguage.getSubTags().isEmpty())) {
                if (variantLanguage.getSubTags().isEmpty()
                        && preferenceLanguage.getSubTags().isEmpty()) {
                    score += 10;
                } else {
                    // Don't change the score
                }
            } else {
                int maxSize = Math.min(preferenceLanguage.getSubTags().size(),
                        variantLanguage.getSubTags().size());
                for (int i = 0; i < maxSize && compatibleLang; i++) {
                    if (preferenceLanguage.getSubTags().get(i)
                            .equalsIgnoreCase(
                                    variantLanguage.getSubTags().get(i))) {
                        // Each subtag contribution to the score
                        // is getting less and less important
                        score += Math.pow(10, 1 - i);
                    } else {
                        // SubTags are different
                        compatibleLang = false;
                    }
                }
            }
        }

        return (compatibleLang ? score : -1.0f);
    }

    /**
     * Returns a matching score between 2 Media types
     * 
     * @param variantMediaType
     * @param preferenceMediaType
     * @return the positive matching score or -1 if the media types are not
     *         compatible
     */
    private float getScore(MediaType variantMediaType,
            MediaType preferenceMediaType) {
        float score = 0.0f;
        boolean comptabibleMediaType = true;

        // 1) Compare the main types
        if (preferenceMediaType.getMainType().equals(
                variantMediaType.getMainType())) {
            score += 1000;
        } else if (!preferenceMediaType.getMainType().equals("*")) {
            comptabibleMediaType = false;
        } else if (!preferenceMediaType.getSubType().equals("*")) {
            // Ranges such as "*/html" are not supported
            // Only "*/*" is acceptable in this case
            comptabibleMediaType = false;
        }

        if (comptabibleMediaType) {
            // 2) Compare the sub types
            if (variantMediaType.getSubType().equals(
                    preferenceMediaType.getSubType())) {
                score += 100;
            } else if (!preferenceMediaType.getSubType().equals("*")) {
                // Sub-type are different
                comptabibleMediaType = false;
            }

            if (comptabibleMediaType
                    && (variantMediaType.getParameters() != null)) {
                // 3) Compare the parameters
                // If current media type is compatible with the
                // current media range then the parameters need to
                // be checked too
                for (Iterator<Parameter> iter3 = variantMediaType
                        .getParameters().iterator(); iter3.hasNext();) {
                    Parameter currentParam = iter3.next();

                    if (isParameterFound(currentParam, preferenceMediaType)) {
                        score++;
                    }
                }
            }

        }
        return (comptabibleMediaType ? score : -1.0f);
    }

    /**
     * Indicates if the searched parameter is specified in the given media
     * range.
     * 
     * @param searchedParam
     *                The searched parameter.
     * @param mediaRange
     *                The media range to inspect.
     * @return True if the searched parameter is specified in the given media
     *         range.
     */
    private boolean isParameterFound(Parameter searchedParam,
            MediaType mediaRange) {
        boolean result = false;

        for (Iterator<Parameter> iter = mediaRange.getParameters().iterator(); !result
                && iter.hasNext();) {
            result = searchedParam.equals(iter.next());
        }

        return result;
    }

    @Override
    public void parse(Logger logger, Form form, Representation webForm) {
        if (webForm != null) {
            FormUtils.parse(logger, form, webForm);
        }
    }

    @Override
    public void parse(Logger logger, Form form, String queryString,
            CharacterSet characterSet, boolean decode, char separator) {
        if ((queryString != null) && !queryString.equals("")) {
            FormUtils.parse(logger, form, queryString, characterSet, decode,
                    separator);
        }
    }

    @Override
    public MediaType parseContentType(String contentType)
            throws IllegalArgumentException {
        try {
            return ContentType.parseContentType(contentType);
        } catch (IOException e) {
            throw new IllegalArgumentException("The content type string \""
                    + contentType + "\" can not be parsed: " + e.getMessage(),
                    e);
        }
    }

    @Override
    public Cookie parseCookie(String cookie) throws IllegalArgumentException {
        CookieReader cr = new CookieReader(logger, cookie);
        try {
            return cr.readCookie();
        } catch (IOException e) {
            throw new IllegalArgumentException("Could not read the cookie", e);
        }
    }

    @Override
    public CookieSetting parseCookieSetting(String cookieSetting)
            throws IllegalArgumentException {
        CookieReader cr = new CookieReader(logger, cookieSetting);
        try {
            return cr.readCookieSetting();
        } catch (IOException e) {
            throw new IllegalArgumentException(
                    "Could not read the cookie setting", e);
        }
    }

    @Override
    public List<Product> parseUserAgent(String userAgent)
            throws IllegalArgumentException {
        List<Product> result = new ArrayList<Product>();

        if (userAgent != null) {
            String token = null;
            String version = null;
            String comment = null;
            char[] tab = userAgent.trim().toCharArray();
            StringBuilder tokenBuilder = new StringBuilder();
            StringBuilder versionBuilder = null;
            StringBuilder commentBuilder = null;
            int index = 0;
            boolean insideToken = true;
            boolean insideVersion = false;
            boolean insideComment = false;

            for (index = 0; index < tab.length; index++) {
                char c = tab[index];
                if (insideToken) {
                    if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')
                            || c == ' ') {
                        tokenBuilder.append(c);
                    } else {
                        token = tokenBuilder.toString().trim();
                        insideToken = false;
                        if (c == '/') {
                            insideVersion = true;
                            versionBuilder = new StringBuilder();
                            version = null;
                        } else if (c == '(') {
                            insideComment = true;
                            commentBuilder = new StringBuilder();
                            comment = null;
                        }
                    }
                } else {
                    if (insideVersion) {
                        if (c != ' ') {
                            versionBuilder.append(c);
                        } else {
                            insideVersion = false;
                            version = versionBuilder.toString();
                        }
                    } else {
                        if (c == '(') {
                            insideComment = true;
                            commentBuilder = new StringBuilder();
                            comment = null;
                        } else {
                            if (insideComment) {
                                if (c == ')') {
                                    insideComment = false;
                                    comment = commentBuilder.toString();
                                    result.add(new Product(token, version,
                                            comment));
                                    comment = null;
                                    insideToken = true;
                                    tokenBuilder = new StringBuilder();
                                    token = null;
                                } else {
                                    commentBuilder.append(c);
                                }
                            } else {
                                result
                                        .add(new Product(token, version,
                                                comment));
                                insideToken = true;
                                tokenBuilder = new StringBuilder();
                                tokenBuilder.append(c);
                                token = null;
                            }
                        }
                    }
                }
            }

            if (insideComment) {
                comment = commentBuilder.toString();
                result.add(new Product(token, version, comment));
            } else {
                if (insideVersion) {
                    version = versionBuilder.toString();
                    result.add(new Product(token, version, null));
                } else {
                    if (insideToken && tokenBuilder.length() > 0) {
                        token = tokenBuilder.toString();
                        result.add(new Product(token, null, null));
                    }
                }
            }
        }

        return result;

    }

    /**
     * Registers the default authentication helpers.
     */
    @SuppressWarnings("deprecation")
    private void registerDefaultAuthentications() {
        getRegisteredAuthentications().add(new HttpBasicHelper());
        getRegisteredAuthentications().add(new HttpDigestHelper());
        getRegisteredAuthentications().add(new SmtpPlainHelper());
        getRegisteredAuthentications().add(new HttpAmazonS3Helper());

        // In order to support the deprecated AWS constant
        // we need to register another instance of S3 helper.
        AuthenticationHelper helper = new HttpAmazonS3Helper();
        helper.setChallengeScheme(ChallengeScheme.HTTP_AWS);
        getRegisteredAuthentications().add(helper);
    }

    /**
     * Registers the default client and server connectors.
     */
    private void registerDefaultConnectors() {
        getRegisteredClients().add(new StreamClientHelper(null));
        getRegisteredClients().add(new ClapClientHelper(null));
        getRegisteredClients().add(new FileClientHelper(null));
        getRegisteredServers().add(new StreamServerHelper(null));
    }

    /**
     * Registers a factory that is used by the URL class to create the
     * {@link URLConnection} instances when the {@link URL#openConnection()} or
     * {@link URL#openStream()} methods are invoked.
     * <p>
     * The implementation is based on the client dispatcher of the current
     * context, as provided by {@link Context#getCurrent()} method.
     */
    public void registerUrlFactory() {
        // Set up an URLStreamHandlerFactory for
        // proper creation of java.net.URL instances
        URL.setURLStreamHandlerFactory(new URLStreamHandlerFactory() {
            public URLStreamHandler createURLStreamHandler(String protocol) {
                URLStreamHandler result = new URLStreamHandler() {

                    @Override
                    protected URLConnection openConnection(URL url)
                            throws IOException {
                        return new URLConnection(url) {

                            @Override
                            public void connect() throws IOException {
                            }

                            @Override
                            public InputStream getInputStream()
                                    throws IOException {
                                InputStream result = null;

                                // Retrieve the current context
                                Context context = Context.getCurrent();

                                if (context != null) {
                                    Response response = context
                                            .getClientDispatcher().get(
                                                    url.toString());

                                    if (response.getStatus().isSuccess()) {
                                        result = response.getEntity()
                                                .getStream();
                                    }
                                }

                                return result;
                            }
                        };
                    }

                };

                return result;
            }

        });
    }

    @Override
    public String toMd5(String target) {
        return SecurityUtils.toMd5(target);
    }

}
