import {CommonModule} from "@angular/common";
import {NgModule} from "@angular/core";
import {PluginInboxClientComponent} from "./plugin-inbox-client.component";
import {Routes} from "@angular/router";
import {PeekModuleFactory} from "@synerty/peek-util-web";

import {
    LoggedInGuard,
    LoggedOutGuard,
    ProfileService,
    UserService
} from "@peek/peek_core_user";

import {ActivityListComponent} from "./activity-list/activity-list.component";
import {TaskListComponent} from "./task-list/task-list.component";


export const pluginRoutes: Routes = [
    {
        path: '',
        component: PluginInboxClientComponent,
        canActivate: [LoggedInGuard]
    },
    {
        path: '**',
        component: PluginInboxClientComponent,
        canActivate: [LoggedInGuard]
    }

];

@NgModule({
    imports: [
        CommonModule,
        PeekModuleFactory.RouterModule.forChild(pluginRoutes),
        ...PeekModuleFactory.FormsModules
    ],
    exports: [],
    providers: [],
    declarations: [PluginInboxClientComponent,
        TaskListComponent,
        ActivityListComponent
    ]
})
export class PluginInboxClientModule {
}