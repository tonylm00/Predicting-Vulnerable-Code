// $Id$
/*
* JBoss, Home of Professional Open Source
* Copyright 2008, Red Hat Middleware LLC, and individual contributors
* by the @authors tag. See the copyright.txt in the distribution for a
* full listing of individual contributors.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
* http://www.apache.org/licenses/LICENSE-2.0
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,  
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/
package org.hibernate.validation.eg;

import javax.validation.constraints.NotNull;

import org.hibernate.validation.constraints.NotEmpty;
import org.hibernate.validation.eg.groups.First;
import org.hibernate.validation.eg.groups.Second;

/**
 * @author Hardy Ferentschik
 */
public class Animal {
	public enum Domain {
		PROKARYOTA, EUKARYOTA
	}

	@NotEmpty(groups = { First.class, Second.class })
	private String name;

	@NotNull(groups = First.class)
	private Domain domain;

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public Domain getDomain() {
		return domain;
	}

	public void setDomain(Domain domain) {
		this.domain = domain;
	}
}