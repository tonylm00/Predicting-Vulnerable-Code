
/*
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *  under the License.
 */
package org.syncope.core.rest.controller;

import org.syncope.core.util.AttributableUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.TypeMismatchException;
import org.springframework.transaction.annotation.Transactional;
import org.syncope.client.to.PropagationTaskTO;
import org.syncope.client.to.SchedTaskTO;
import org.syncope.client.to.SyncTaskTO;
import org.syncope.client.to.TaskTO;
import org.syncope.core.persistence.beans.NotificationTask;
import org.syncope.core.persistence.beans.PropagationTask;
import org.syncope.core.persistence.beans.SchedTask;
import org.syncope.core.persistence.beans.SyncTask;
import org.syncope.core.persistence.beans.Task;
import org.syncope.core.util.TaskUtil;

@Transactional(rollbackFor = {
    Throwable.class
})
public abstract class AbstractController {

    /**
     * Logger.
     */
    protected static final Logger LOG =
            LoggerFactory.getLogger(AbstractController.class);

    protected AttributableUtil getAttributableUtil(final String kind) {
        AttributableUtil result = null;

        try {
            result = AttributableUtil.valueOf(kind.toUpperCase());
        } catch (Exception e) {
            LOG.error("Attributable not supported: " + kind);

            throw new TypeMismatchException(kind, AttributableUtil.class, e);
        }

        return result;
    }

    protected TaskUtil getTaskUtil(final String kind) {
        TaskUtil result = null;

        try {
            result = TaskUtil.valueOf(kind.toUpperCase());
        } catch (Exception e) {
            LOG.error("Task not supported: " + kind);

            throw new TypeMismatchException(kind, TaskUtil.class, e);
        }

        return result;
    }

    protected TaskUtil getTaskUtil(final Task task) {
        TaskUtil result = (task instanceof PropagationTask)
                ? TaskUtil.PROPAGATION
                : (task instanceof NotificationTask)
                ? TaskUtil.NOTIFICATION
                : (task instanceof SyncTask)
                ? TaskUtil.SYNC
                : (task instanceof SchedTask)
                ? TaskUtil.SCHED
                : null;

        if (result == null) {
            LOG.error("Task not supported: " + task.getClass().getName());

            throw new TypeMismatchException(task.getClass().getName(),
                    TaskUtil.class);
        }

        return result;
    }

    protected TaskUtil getTaskUtil(final TaskTO taskTO) {
        TaskUtil result = (taskTO instanceof PropagationTaskTO)
                ? TaskUtil.PROPAGATION
                : (taskTO instanceof SyncTaskTO)
                ? TaskUtil.SYNC
                : (taskTO instanceof SchedTaskTO)
                ? TaskUtil.SCHED
                : null;

        if (result == null) {
            LOG.error("Task not supported: " + taskTO.getClass().getName());

            throw new TypeMismatchException(taskTO.getClass().getName(),
                    TaskUtil.class);
        }

        return result;
    }
}
