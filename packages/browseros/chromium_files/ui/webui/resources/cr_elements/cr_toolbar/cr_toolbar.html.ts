// Copyright 2024 The Chromium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

import { html, nothing } from '//resources/lit/v3_0/lit.rollup.js';

import type { CrToolbarElement } from './cr_toolbar.js';

export function getHtml(this: CrToolbarElement) {
  // clang-format off
  return html`
<div id="leftContent">
  <div id="leftSpacer" style="display: flex; align-items: center;">
    ${this.showMenu ? html`
      <cr-icon-button id="menuButton" class="no-overlap"
          iron-icon="cr20:menu" @click="${this.onMenuClick_}"
          aria-label="${this.menuLabel || nothing}"
          title="${this.menuLabel}">
      </cr-icon-button>` : ''}
    <slot name="product-logo">
      <svg id="product-logo" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1024 1024" xml:space="preserve" role="presentation" style="width: 32px; height: 32px; object-fit: contain; margin-inline-end: 8px; display: block;">
        <style type="text/css">
          .st0{fill:none;}
          .st1{clip-path:url(#SVGID_3_);fill:none;stroke:#1D79FF;stroke-width:209;stroke-miterlimit:10;}
          .st2{clip-path:url(#SVGID_5_);fill:none;stroke:#1D79FF;stroke-width:209;stroke-miterlimit:10;}
        </style>
        <g>
          <g>
            <circle id="SVGID_1_" class="st0" cx="513.3" cy="510.8" r="454.9"/>
          </g>
          <g>
            <g>
              <defs>
                <circle id="SVGID_2_" cx="513.3" cy="510.8" r="454.9"/>
              </defs>
              <clipPath id="SVGID_3_">
                <use xlink:href="#SVGID_2_" style="overflow:visible;"/>
              </clipPath>
              <circle class="st1" cx="758.2" cy="988.4" r="411.5"/>
            </g>
          </g>
          <g>
            <g>
              <defs>
                <circle id="SVGID_4_" cx="513.3" cy="510.8" r="454.9"/>
              </defs>
              <clipPath id="SVGID_5_">
                <use xlink:href="#SVGID_4_" style="overflow:visible;"/>
              </clipPath>
              <circle class="st2" cx="262" cy="81.4" r="411.5"/>
            </g>
          </g>
        </g>
      </svg>
    </slot>
    <h1 style="margin: 0; line-height: 1;">${this.pageName}</h1>
  </div>
</div>

<div id="centeredContent" ?hidden="${!this.showSearch}">
  <cr-toolbar-search-field id="search" ?narrow="${this.narrow}"
      label="${this.searchPrompt}" clear-label="${this.clearLabel}"
      ?spinner-active="${this.spinnerActive}"
      ?showing-search="${this.showingSearch_}"
      @showing-search-changed="${this.onShowingSearchChanged_}"
      ?autofocus="${this.autofocus}" icon-override="${this.searchIconOverride}"
      input-aria-description="${this.searchInputAriaDescription}">
  </cr-toolbar-search-field>
</div>

<div id="rightContent">
  <div id="rightSpacer">
    <slot></slot>
  </div>
</div>`;
  // clang-format on
}
