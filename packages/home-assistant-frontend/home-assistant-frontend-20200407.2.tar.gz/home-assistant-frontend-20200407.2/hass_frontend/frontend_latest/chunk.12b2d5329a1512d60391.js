(self.webpackJsonp=self.webpackJsonp||[]).push([[125],{793:function(e,a,l){"use strict";l.r(a);l(164);var o=l(4),r=l(32);l(139),l(109);customElements.define("ha-panel-iframe",class extends r.a{static get template(){return o.a`
      <style include="ha-style">
        iframe {
          border: 0;
          width: 100%;
          position: absolute;
          height: calc(100% - 64px);
          background-color: var(--primary-background-color);
        }
      </style>
      <app-toolbar>
        <ha-menu-button hass="[[hass]]" narrow="[[narrow]]"></ha-menu-button>
        <div main-title>[[panel.title]]</div>
      </app-toolbar>

      <iframe
        src="[[panel.config.url]]"
        sandbox="allow-forms allow-popups allow-pointer-lock allow-same-origin allow-scripts"
        allowfullscreen="true"
        webkitallowfullscreen="true"
        mozallowfullscreen="true"
      ></iframe>
    `}static get properties(){return{hass:Object,narrow:Boolean,panel:Object}}})}}]);
//# sourceMappingURL=chunk.12b2d5329a1512d60391.js.map