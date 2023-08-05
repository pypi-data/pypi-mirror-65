import {BrowserModule} from "@angular/platform-browser";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";

import {NgModule} from "@angular/core";
import {FormsModule} from "@angular/forms";
import {Ng2BalloonMsgService} from "@synerty/ng2-balloon-msg";
import {Ng2BalloonMsgModule} from "@synerty/ng2-balloon-msg-web";
import {
    TupleStorageFactoryService,
    VortexService,
    VortexStatusService,
    WebSqlFactoryService
} from "@synerty/vortexjs";

import {
    TupleStorageFactoryServiceWeb,
    WebSqlBrowserFactoryService
} from "@synerty/vortexjs/index-browser";
import {AppRoutingModule} from "./app/app-routing.module";
import {AppComponent} from "./app/app.component";
import {DashboardModule} from "./app/dashboard/dashboard.module";
import {NavbarModule} from "./app/navbar/navbar.module";
import {PluginRootComponent} from "./app/plugin-root.component"
import {en_US, NgZorroAntdModule, NZ_I18N} from 'ng-zorro-antd';

import {AngularFontAwesomeModule} from "angular-font-awesome/dist/angular-font-awesome";

import {ACE_CONFIG, AceConfigInterface, AceModule} from 'ngx-ace-wrapper';
/** config angular i18n **/
import {registerLocaleData} from '@angular/common';
import en from '@angular/common/locales/en';

const DEFAULT_ACE_CONFIG: AceConfigInterface = {};


registerLocaleData(en);

@NgModule({
    declarations: [
        AppComponent,
        PluginRootComponent
    ],
    imports: [
        AceModule,
        BrowserModule,
        BrowserAnimationsModule,
        FormsModule,
        AngularFontAwesomeModule,
        AppRoutingModule,
        Ng2BalloonMsgModule,
        DashboardModule,
        NavbarModule,
        NgZorroAntdModule
    ],
    providers: [
        {provide: NZ_I18N, useValue: en_US},
        {
            provide: ACE_CONFIG,
            useValue: DEFAULT_ACE_CONFIG
        },
        {provide: WebSqlFactoryService, useClass: WebSqlBrowserFactoryService},
        {provide: TupleStorageFactoryService, useClass: TupleStorageFactoryServiceWeb},
        Ng2BalloonMsgService, VortexService, VortexStatusService],
    bootstrap: [AppComponent]
})
export class AppModule {

}
