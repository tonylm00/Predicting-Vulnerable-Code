/*
 * Copyright 2014-present Facebook, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

package com.facebook.buck.cxx;

import com.facebook.buck.model.HasBuildTarget;
import com.facebook.buck.rules.SourcePath;
import com.facebook.buck.rules.TargetGraph;
import com.google.common.collect.ImmutableMap;

/**
 * Interface for {@link com.facebook.buck.rules.BuildRule} objects (e.g. C++ libraries) which can
 * contribute to the top-level link of a native binary (e.g. C++ binary).
 */
public interface NativeLinkable extends HasBuildTarget {

  Iterable<? extends NativeLinkable> getNativeLinkableDeps(CxxPlatform cxxPlatform);

  Iterable<? extends NativeLinkable> getNativeLinkableExportedDeps(CxxPlatform cxxPlatform);

  NativeLinkableInput getNativeLinkableInput(
      TargetGraph targetGraph,
      CxxPlatform cxxPlatform,
      Linker.LinkableDepType type);

  Linkage getPreferredLinkage(CxxPlatform cxxPlatform);

  /**
   * @return a map of shared library SONAME to shared library path for the given
   *     {@link CxxPlatform}.
   */
  ImmutableMap<String, SourcePath> getSharedLibraries(
      TargetGraph targetGraph,
      CxxPlatform cxxPlatform);

  enum Linkage {
    ANY,
    STATIC,
  }

}
