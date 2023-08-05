// Angular
import {BrowserModule} from "@angular/platform-browser";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";

import {NgModule} from "@angular/core";
import {RouterModule} from "@angular/router";
// @synerty
import {Ng2BalloonMsgModule} from "@synerty/ng2-balloon-msg-web";
import {PeekModuleFactory} from "@synerty/peek-util-web";
import {
    TupleActionPushOfflineSingletonService,
    TupleDataObservableNameService,
    TupleOfflineStorageNameService,
    TupleStorageFactoryService,
    WebSqlFactoryService
} from "@synerty/vortexjs";

import {
    TupleStorageFactoryServiceWeb,
    WebSqlBrowserFactoryService
} from "@synerty/vortexjs/index-browser";
// Routes
import {staticRoutes} from "./app/app.routes";
import {peekRootServices} from "./app/app.services";
// This app
import {AppComponent} from "./app/app.component";
import {MainHomeComponent} from "./app/main-home/main-home.component";
import {MainConfigComponent} from "./app/main-config/main-config.component";
import {MainSidebarComponent} from "./app/main-sidebar/main-sidebar.component";
import {UnknownRouteComponent} from "./app/unknown-route/unknown-route.component";
import {pluginRootModules} from "./plugin-root-modules";
import {pluginRootServices} from "./plugin-root-services";
import {PluginRootComponent} from "./app/plugin-root.component";
import {en_US, NgZorroAntdModule, NZ_I18N} from 'ng-zorro-antd';
/** config angular i18n **/
import {registerLocaleData} from '@angular/common';
import en from '@angular/common/locales/en';
import {SearchModule} from "peek_core_search/search.module";

registerLocaleData(en);

export function tupleDataObservableNameServiceFactory() {
    return new TupleDataObservableNameService("peek_client", {"plugin": "peek_client"});
}

export function tupleOfflineStorageNameServiceFactory() {
    return new TupleOfflineStorageNameService("peek_client");
}


@NgModule({
    declarations: [AppComponent,
        MainHomeComponent,
        MainConfigComponent,
        MainSidebarComponent,
        UnknownRouteComponent,
        PluginRootComponent],
    bootstrap: [AppComponent],
    imports: [
        RouterModule,
        PeekModuleFactory.RouterModule.forRoot(staticRoutes),
        BrowserModule,
        BrowserAnimationsModule,
        ...PeekModuleFactory.FormsModules,
        Ng2BalloonMsgModule,
        ...pluginRootModules,
        NgZorroAntdModule,
        SearchModule
    ],
    providers: [
        {provide: NZ_I18N, useValue: en_US},
        {provide: WebSqlFactoryService, useClass: WebSqlBrowserFactoryService},
        {provide: TupleStorageFactoryService, useClass: TupleStorageFactoryServiceWeb},
        TupleActionPushOfflineSingletonService,


        ...peekRootServices,
        ...pluginRootServices,
    ]
})
export class AppWebModule {

}
