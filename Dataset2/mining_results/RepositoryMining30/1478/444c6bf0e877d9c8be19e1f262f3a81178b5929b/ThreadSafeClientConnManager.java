/*
 * ====================================================================
 *
 *  Licensed to the Apache Software Foundation (ASF) under one or more
 *  contributor license agreements.  See the NOTICE file distributed with
 *  this work for additional information regarding copyright ownership.
 *  The ASF licenses this file to You under the Apache License, Version 2.0
 *  (the "License"); you may not use this file except in compliance with
 *  the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 * ====================================================================
 *
 * This software consists of voluntary contributions made by many
 * individuals on behalf of the Apache Software Foundation.  For more
 * information on the Apache Software Foundation, please see
 * <http://www.apache.org/>.
 *
 */

package org.apache.http.impl.conn.tsccm;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.http.annotation.ThreadSafe;
import org.apache.http.conn.params.ConnPerRouteBean;
import org.apache.http.conn.routing.HttpRoute;
import org.apache.http.conn.scheme.SchemeRegistry;
import org.apache.http.conn.ClientConnectionManager;
import org.apache.http.conn.ClientConnectionOperator;
import org.apache.http.conn.ClientConnectionRequest;
import org.apache.http.conn.ConnectionPoolTimeoutException;
import org.apache.http.conn.ManagedClientConnection;
import org.apache.http.conn.OperatedClientConnection;
import org.apache.http.params.HttpParams;
import org.apache.http.impl.conn.DefaultClientConnectionOperator;
import org.apache.http.impl.conn.SchemeRegistryFactory;

/**
 * Manages a pool of {@link OperatedClientConnection client connections} and
 * is able to service connection requests from multiple execution threads.
 * Connections are pooled on a per route basis. A request for a route which
 * already the manager has persistent connections for available in the pool
 * will be services by leasing a connection from the pool rather than
 * creating a brand new connection.
 * <p>
 * ThreadSafeClientConnManager maintains a maximum limit of connection on
 * a per route basis and in total. Per default this implementation will
 * create no more than than 2 concurrent connections per given route
 * and no more 20 connections in total. For many real-world applications
 * these limits may prove too constraining, especially if they use HTTP
 * as a transport protocol for their services. Connection limits, however,
 * can be adjusted using HTTP parameters.
 *
 * @since 4.0
 */
@ThreadSafe
public class ThreadSafeClientConnManager implements ClientConnectionManager {

    private final Log log;

    /** The schemes supported by this connection manager. */
    protected final SchemeRegistry schemeRegistry; // @ThreadSafe

    @Deprecated
    protected final AbstractConnPool connectionPool;

    /** The pool of connections being managed. */
    protected final ConnPoolByRoute pool;

    /** The operator for opening and updating connections. */
    protected final ClientConnectionOperator connOperator; // DefaultClientConnectionOperator is @ThreadSafe

    protected final ConnPerRouteBean connPerRoute;

    /**
     * Creates a new thread safe connection manager.
     *
     * @param schreg    the scheme registry.
     */
    public ThreadSafeClientConnManager(final SchemeRegistry schreg) {
        this(schreg, -1, TimeUnit.MILLISECONDS);
    }

    /**
     * @since 4.1
     */
    public ThreadSafeClientConnManager() {
        this(SchemeRegistryFactory.createDefault());
    }

    /**
     * Creates a new thread safe connection manager.
     *
     * @param schreg    the scheme registry.
     * @param connTTL   max connection lifetime, <=0 implies "infinity"
     * @param connTTLTimeUnit   TimeUnit of connTTL
     *
     * @since 4.1
     */
    public ThreadSafeClientConnManager(final SchemeRegistry schreg,
            long connTTL, TimeUnit connTTLTimeUnit) {
        this(schreg, connTTL, connTTLTimeUnit, new ConnPerRouteBean());
    }

    /**
     * Creates a new thread safe connection manager.
     *
     * @param schreg    the scheme registry.
     * @param connTTL   max connection lifetime, <=0 implies "infinity"
     * @param connTTLTimeUnit   TimeUnit of connTTL
     * @param connPerRoute    mapping of maximum connections per route,
     *   provided as a dependency so it can be managed externally, e.g.
     *   for dynamic connection pool size management.
     *
     * @since 4.2
     */
    public ThreadSafeClientConnManager(final SchemeRegistry schreg,
            long connTTL, TimeUnit connTTLTimeUnit, ConnPerRouteBean connPerRoute) {
        super();
        if (schreg == null) {
            throw new IllegalArgumentException("Scheme registry may not be null");
        }
        this.log = LogFactory.getLog(getClass());
        this.schemeRegistry = schreg;
        this.connPerRoute = connPerRoute;
        this.connOperator = createConnectionOperator(schreg);
        this.pool = createConnectionPool(connTTL, connTTLTimeUnit) ;
        this.connectionPool = this.pool;        
    }

    /**
     * Creates a new thread safe connection manager.
     *
     * @param params    the parameters for this manager.
     * @param schreg    the scheme registry.
     *
     * @deprecated use {@link ThreadSafeClientConnManager#ThreadSafeClientConnManager(SchemeRegistry)}
     */
    @Deprecated
    public ThreadSafeClientConnManager(HttpParams params,
                                       SchemeRegistry schreg) {
        if (schreg == null) {
            throw new IllegalArgumentException("Scheme registry may not be null");
        }
        this.log = LogFactory.getLog(getClass());
        this.schemeRegistry = schreg;
        this.connPerRoute = new ConnPerRouteBean();
        this.connOperator = createConnectionOperator(schreg);
        this.pool = (ConnPoolByRoute) createConnectionPool(params) ;
        this.connectionPool = this.pool;
    }

    @Override
    protected void finalize() throws Throwable {
        try {
            shutdown();
        } finally {
            super.finalize();
        }
    }

    /**
     * Hook for creating the connection pool.
     *
     * @return  the connection pool to use
     *
     * @deprecated use #createConnectionPool(long, TimeUnit))
     */
    @Deprecated
    protected AbstractConnPool createConnectionPool(final HttpParams params) {
        return new ConnPoolByRoute(connOperator, params);
    }

    /**
     * Hook for creating the connection pool.
     *
     * @return  the connection pool to use
     *
     * @since 4.1
     */
    protected ConnPoolByRoute createConnectionPool(long connTTL, TimeUnit connTTLTimeUnit) {
        return new ConnPoolByRoute(connOperator, connPerRoute, 20, connTTL, connTTLTimeUnit);
    }

    /**
     * Hook for creating the connection operator.
     * It is called by the constructor.
     * Derived classes can override this method to change the
     * instantiation of the operator.
     * The default implementation here instantiates
     * {@link DefaultClientConnectionOperator DefaultClientConnectionOperator}.
     *
     * @param schreg    the scheme registry.
     *
     * @return  the connection operator to use
     */
    protected ClientConnectionOperator
        createConnectionOperator(SchemeRegistry schreg) {

        return new DefaultClientConnectionOperator(schreg);// @ThreadSafe
    }

    public SchemeRegistry getSchemeRegistry() {
        return this.schemeRegistry;
    }

    public ClientConnectionRequest requestConnection(
            final HttpRoute route,
            final Object state) {

        final PoolEntryRequest poolRequest = pool.requestPoolEntry(
                route, state);

        return new ClientConnectionRequest() {

            public void abortRequest() {
                poolRequest.abortRequest();
            }

            public ManagedClientConnection getConnection(
                    long timeout, TimeUnit tunit) throws InterruptedException,
                    ConnectionPoolTimeoutException {
                if (route == null) {
                    throw new IllegalArgumentException("Route may not be null.");
                }

                if (log.isDebugEnabled()) {
                    log.debug("Get connection: " + route + ", timeout = " + timeout);
                }

                BasicPoolEntry entry = poolRequest.getPoolEntry(timeout, tunit);
                return new BasicPooledConnAdapter(ThreadSafeClientConnManager.this, entry);
            }

        };

    }

    public void releaseConnection(ManagedClientConnection conn, long validDuration, TimeUnit timeUnit) {

        if (!(conn instanceof BasicPooledConnAdapter)) {
            throw new IllegalArgumentException
                ("Connection class mismatch, " +
                 "connection not obtained from this manager.");
        }
        BasicPooledConnAdapter hca = (BasicPooledConnAdapter) conn;
        if ((hca.getPoolEntry() != null) && (hca.getManager() != this)) {
            throw new IllegalArgumentException
                ("Connection not obtained from this manager.");
        }
        synchronized (hca) {
            BasicPoolEntry entry = (BasicPoolEntry) hca.getPoolEntry();
            if (entry == null) {
                return;
            }
            try {
                // make sure that the response has been read completely
                if (hca.isOpen() && !hca.isMarkedReusable()) {
                    // In MTHCM, there would be a call to
                    // SimpleHttpConnectionManager.finishLastResponse(conn);
                    // Consuming the response is handled outside in 4.0.

                    // make sure this connection will not be re-used
                    // Shut down rather than close, we might have gotten here
                    // because of a shutdown trigger.
                    // Shutdown of the adapter also clears the tracked route.
                    hca.shutdown();
                }
            } catch (IOException iox) {
                if (log.isDebugEnabled())
                    log.debug("Exception shutting down released connection.",
                              iox);
            } finally {
                boolean reusable = hca.isMarkedReusable();
                if (log.isDebugEnabled()) {
                    if (reusable) {
                        log.debug("Released connection is reusable.");
                    } else {
                        log.debug("Released connection is not reusable.");
                    }
                }
                hca.detach();
                pool.freeEntry(entry, reusable, validDuration, timeUnit);
            }
        }
    }

    public void shutdown() {
        log.debug("Shutting down");
        pool.shutdown();
    }

    /**
     * Gets the total number of pooled connections for the given route.
     * This is the total number of connections that have been created and
     * are still in use by this connection manager for the route.
     * This value will not exceed the maximum number of connections per host.
     *
     * @param route     the route in question
     *
     * @return  the total number of pooled connections for that route
     */
    public int getConnectionsInPool(final HttpRoute route) {
        return pool.getConnectionsInPool(route);
    }

    /**
     * Gets the total number of pooled connections.  This is the total number of
     * connections that have been created and are still in use by this connection
     * manager.  This value will not exceed the maximum number of connections
     * in total.
     *
     * @return the total number of pooled connections
     */
    public int getConnectionsInPool() {
        return pool.getConnectionsInPool();
    }

    public void closeIdleConnections(long idleTimeout, TimeUnit tunit) {
        if (log.isDebugEnabled()) {
            log.debug("Closing connections idle longer than " + idleTimeout + " " + tunit);
        }
        pool.closeIdleConnections(idleTimeout, tunit);
    }

    public void closeExpiredConnections() {
        log.debug("Closing expired connections");
        pool.closeExpiredConnections();
    }

    /**
     * since 4.1
     */
    public int getMaxTotal() {
        return pool.getMaxTotalConnections();
    }

    /**
     * since 4.1
     */
    public void setMaxTotal(int max) {
        pool.setMaxTotalConnections(max);
    }

    /**
     * @since 4.1
     */
    public int getDefaultMaxPerRoute() {
        return connPerRoute.getDefaultMaxPerRoute();
    }

    /**
     * @since 4.1
     */
    public void setDefaultMaxPerRoute(int max) {
        connPerRoute.setDefaultMaxPerRoute(max);
    }

    /**
     * @since 4.1
     */
    public int getMaxForRoute(final HttpRoute route) {
        return connPerRoute.getMaxForRoute(route);
    }

    /**
     * @since 4.1
     */
    public void setMaxForRoute(final HttpRoute route, int max) {
        connPerRoute.setMaxForRoute(route, max);
    }

}

