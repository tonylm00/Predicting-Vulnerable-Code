/*
 * Copyright 2002-2016 the original author or authors.
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
package org.springframework.security.config.http;

import org.springframework.beans.factory.config.BeanDefinition;
import org.springframework.beans.factory.support.BeanDefinitionBuilder;
import org.springframework.beans.factory.support.RootBeanDefinition;
import org.springframework.security.web.util.matcher.AntPathRequestMatcher;
import org.springframework.security.web.util.matcher.AnyRequestMatcher;
import org.springframework.security.web.util.matcher.RegexRequestMatcher;
import org.springframework.security.web.util.matcher.RequestMatcher;
import org.springframework.util.StringUtils;
import org.w3c.dom.Element;

/**
 * Defines the {@link RequestMatcher} types supported by the namespace.
 *
 * @author Luke Taylor
 * @since 3.1
 */
public enum MatcherType {
	ant(AntPathRequestMatcher.class), regex(RegexRequestMatcher.class), ciRegex(
			RegexRequestMatcher.class);

	private static final String ATT_MATCHER_TYPE = "request-matcher";

	private final Class<? extends RequestMatcher> type;

	MatcherType(Class<? extends RequestMatcher> type) {
		this.type = type;
	}

	public BeanDefinition createMatcher(String path, String method) {
		if (("/**".equals(path) || "**".equals(path)) && method == null) {
			return new RootBeanDefinition(AnyRequestMatcher.class);
		}

		BeanDefinitionBuilder matcherBldr = BeanDefinitionBuilder
				.rootBeanDefinition(type);

		matcherBldr.addConstructorArgValue(path);
		matcherBldr.addConstructorArgValue(method);

		if (this == ciRegex) {
			matcherBldr.addConstructorArgValue(true);
		}

		return matcherBldr.getBeanDefinition();
	}

	static MatcherType fromElement(Element elt) {
		if (StringUtils.hasText(elt.getAttribute(ATT_MATCHER_TYPE))) {
			return valueOf(elt.getAttribute(ATT_MATCHER_TYPE));
		}

		return ant;
	}
}