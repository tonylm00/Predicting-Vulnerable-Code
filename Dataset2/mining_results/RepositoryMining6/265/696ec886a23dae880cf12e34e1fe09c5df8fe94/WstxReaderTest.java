/*
 * Copyright (C) 2011, 2015 XStream Committers.
 * All rights reserved.
 *
 * The software in this package is published under the terms of the BSD
 * style license a copy of which has been included with this distribution in
 * the LICENSE.txt file.
 * 
 * Created on 30. September 2011 by Joerg Schaible
 */
package com.thoughtworks.xstream.io.xml;

import com.thoughtworks.xstream.XStreamException;
import com.thoughtworks.xstream.io.HierarchicalStreamDriver;
import com.thoughtworks.xstream.io.HierarchicalStreamReader;

import java.io.StringReader;

public class WstxReaderTest extends AbstractXMLReaderTest {
    
    private HierarchicalStreamDriver driver = new WstxDriver();

    // factory method
    protected HierarchicalStreamReader createReader(String xml) throws Exception {
        return driver.createReader(new StringReader(xml));
    }

    @Override
    public void testIsXXEVulnerable() throws Exception {
        try {
            super.testIsXXEVulnerable();
            fail("Thrown " + XStreamException.class.getName() + " expected");
        } catch (final XStreamException e) {
            final String message = e.getMessage();
            if (message.contains("Package")) {
                throw e;
            }
        }
    }

    // inherits tests from superclass
}
