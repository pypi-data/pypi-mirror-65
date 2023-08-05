import {NgModule} from "@angular/core";
import {Route, RouterModule, Routes} from "@angular/router";
import {DashboardComponent} from "./dashboard/dashboard.component";
import {ComponentLifecycleEventEmitter, Tuple} from "@synerty/vortexjs";
import {pluginAppRoutes} from "../plugin-app-routes";
import {pluginCfgRoutes} from "../plugin-cfg-routes";


export const dashboardRoute: Route = {
    path: '',
    component: DashboardComponent
};


const staticRoutes: Routes = [
    dashboardRoute,
    // environmentRoute,
    {
        path: '**',
        component: DashboardComponent

    }
];


class PluginRoutesTuple extends Tuple {
    constructor() {
        super('peek_server.PluginRoutesTuple');
    }

    pluginName: string;
    lazyLoadModulePath: string;
}


@NgModule({
    imports: [RouterModule.forRoot([
        ...pluginAppRoutes,
        ...pluginCfgRoutes,
        ...staticRoutes
    ])],
    exports: [RouterModule],
    providers: []
})
export class AppRoutingModule extends ComponentLifecycleEventEmitter {
}
