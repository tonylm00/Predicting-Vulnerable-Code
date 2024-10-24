/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.catalina.websocket;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.CharBuffer;

import org.apache.coyote.http11.upgrade.UpgradeOutbound;
import org.apache.tomcat.util.buf.B2CConverter;

public class WsOutbound {

    private static final int DEFAULT_BUFFER_SIZE = 8192;

    private UpgradeOutbound upgradeOutbound;
    private ByteBuffer bb;
    private CharBuffer cb;
    private boolean closed = false;
    protected Boolean text = null;
    protected boolean firstFrame = true;


    public WsOutbound(UpgradeOutbound upgradeOutbound) {
        this.upgradeOutbound = upgradeOutbound;
        // TODO: Make buffer size configurable
        this.bb = ByteBuffer.allocate(DEFAULT_BUFFER_SIZE);
        this.cb = CharBuffer.allocate(DEFAULT_BUFFER_SIZE);
    }


    public void writeBinaryData(int b) throws IOException {
        if (bb.position() == bb.capacity()) {
            doFlush(false);
        }
        if (text == null) {
            text = Boolean.FALSE;
        } else if (text == Boolean.TRUE) {
            // Flush the character data
            flush();
            text = Boolean.FALSE;
        }
        bb.put((byte) (b & 0xFF));
    }


    public void writeTextData(char c) throws IOException {
        if (cb.position() == cb.capacity()) {
            doFlush(false);
        }

        if (text == null) {
            text = Boolean.TRUE;
        } else if (text == Boolean.FALSE) {
            // Flush the binary data
            flush();
            text = Boolean.TRUE;
        }
        cb.append(c);
    }


    public void writeBinaryMessage(ByteBuffer msgBb) throws IOException {
        if (text != null) {
            // Empty the buffer
            flush();
        }
        text = Boolean.FALSE;
        doWriteBinary(msgBb, true);
    }


    public void writeTextMessage(CharBuffer msgCb) throws IOException {
        if (text != null) {
            // Empty the buffer
            flush();
        }
        text = Boolean.TRUE;
        doWriteText(msgCb, true);
    }


    public void flush() throws IOException {
        doFlush(true);
    }

    private void doFlush(boolean finalFragment) throws IOException {
        if (text == null) {
            // No data
            return;
        }
        if (text.booleanValue()) {
            doWriteText(cb, finalFragment);
        } else {
            doWriteBinary(bb, finalFragment);
        }
    }


    public void close(int status, ByteBuffer data) throws IOException {
        // TODO Think about threading requirements for writing. This is not
        // currently thread safe and writing almost certainly needs to be.
        if (closed) {
            return;
        }
        closed = true;

        doFlush(true);

        upgradeOutbound.write(0x88);
        if (status == 0) {
            upgradeOutbound.write(0);
        } else {
            upgradeOutbound.write(2 + data.limit());
            upgradeOutbound.write(status >>> 8);
            upgradeOutbound.write(status);
            upgradeOutbound.write(data.array(), 0, data.limit());
        }
        upgradeOutbound.flush();

        bb = null;
        cb = null;
        upgradeOutbound = null;
    }

    protected void doWriteBinary(ByteBuffer buffer, boolean finalFragment)
            throws IOException {

        // Work out the first byte
        int first = 0x00;
        if (finalFragment) {
            first = first + 0x80;
        }
        if (firstFrame) {
            if (text.booleanValue()) {
                first = first + 0x1;
            } else {
                first = first + 0x2;
            }
        }
        // Continuation frame is OpCode 0
        upgradeOutbound.write(first);

        if (buffer.limit() < 126) {
            upgradeOutbound.write(buffer.limit());
        } else if (buffer.limit() < 65536) {
            upgradeOutbound.write(126);
            upgradeOutbound.write(buffer.limit() >>> 8);
            upgradeOutbound.write(buffer.limit() & 0xFF);
        } else {
            // Will never be more than 2^31-1
            upgradeOutbound.write(127);
            upgradeOutbound.write(0);
            upgradeOutbound.write(0);
            upgradeOutbound.write(0);
            upgradeOutbound.write(0);
            upgradeOutbound.write(buffer.limit() >>> 24);
            upgradeOutbound.write(buffer.limit() >>> 16);
            upgradeOutbound.write(buffer.limit() >>> 8);
            upgradeOutbound.write(buffer.limit() & 0xFF);

        }

        // Write the content
        upgradeOutbound.write(buffer.array(), 0, buffer.limit());
        upgradeOutbound.flush();

        // Reset
        if (finalFragment) {
            text = null;
            firstFrame = true;
        } else {
            firstFrame = false;
        }
        bb.clear();
    }


    protected void doWriteText(CharBuffer buffer, boolean finalFragment)
            throws IOException {
        do {
            B2CConverter.UTF_8.newEncoder().encode(buffer, bb, true);
            bb.flip();
            if (buffer.hasRemaining()) {
                doWriteBinary(bb, false);
            } else {
                doWriteBinary(bb, finalFragment);
            }
        } while (buffer.hasRemaining());

        // Reset
        cb.clear();
    }
}
