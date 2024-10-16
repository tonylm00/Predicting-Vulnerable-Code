/*
 * Copyright 2005-2013 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.springframework.ldap.repository;

import org.springframework.data.repository.Repository;
import org.springframework.data.repository.core.support.RepositoryFactoryBeanSupport;
import org.springframework.data.repository.core.support.RepositoryFactorySupport;
import org.springframework.ldap.core.LdapOperations;
import org.springframework.util.Assert;

import javax.naming.Name;

/**
 * {@link org.springframework.beans.factory.FactoryBean} to create {@link LdapRepository} instances.
 *
 * @author Mattias Hellborg Arthursson
 * @since 2.0
 */
public class LdapRepositoryFactoryBean<T extends Repository<S, Name>, S> extends RepositoryFactoryBeanSupport<T, S, Name> {
    private LdapOperations ldapOperations;

    public void setLdapOperations(LdapOperations ldapOperations) {
        this.ldapOperations = ldapOperations;
    }

    @Override
    protected RepositoryFactorySupport createRepositoryFactory() {
        return new LdapRepositoryFactory(ldapOperations);
    }

    @Override
    public void afterPropertiesSet() {
        super.afterPropertiesSet();
        Assert.notNull(ldapOperations, "LdapOperations must be set");
    }
}
