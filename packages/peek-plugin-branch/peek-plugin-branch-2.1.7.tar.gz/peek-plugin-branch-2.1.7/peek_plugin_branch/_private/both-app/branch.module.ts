import {CommonModule} from "@angular/common";
import {NgModule} from "@angular/core";
import {Routes} from "@angular/router";

// Import a small abstraction library to switch between nativescript and web
import {PeekModuleFactory} from "@synerty/peek-util-web";

// Import the default route component
import {BranchComponent} from "./branch.component";

// Import the required classes from VortexJS
import {
    TupleOfflineStorageNameService,
    TupleOfflineStorageService
} from "@synerty/vortexjs";

// Import the names we need for the
import {
    branchTupleOfflineServiceName
} from "@peek/peek_plugin_branch/_private/PluginNames";

// Import the required classes from VortexJS
import {
    TupleDataObservableNameService,
    TupleDataObserverService,
    TupleDataOfflineObserverService
} from "@synerty/vortexjs";

// Import the names we need for the

import {BranchDetailComponent} from "./branch-detail/branch-detail.component";

import {
    branchObservableName,
    branchFilt
} from "@peek/peek_plugin_branch/_private/PluginNames";

// Import the required classes from VortexJS
import {
    TupleActionPushNameService,
    TupleActionPushOfflineService,
    TupleActionPushService
} from "@synerty/vortexjs";

// Import the names we need for the
import {
    branchActionProcessorName
} from "@peek/peek_plugin_branch/_private";


export function tupleActionPushNameServiceFactory() {
    return new TupleActionPushNameService(
        branchActionProcessorName, branchFilt);
}

export function tupleDataObservableNameServiceFactory() {
    return new TupleDataObservableNameService(
        branchObservableName, branchFilt);
}

export function tupleOfflineStorageNameServiceFactory() {
    return new TupleOfflineStorageNameService(branchTupleOfflineServiceName);
}

// Define the child routes for this plugin
export const pluginRoutes: Routes = [
    {
        path: 'branchdetails',
        component: BranchDetailComponent
    },
    {
        path: '',
        pathMatch: 'full',
        component: BranchComponent
    }

];

// Define the root module for this plugin.
// This module is loaded by the lazy loader, what ever this defines is what is started.
// When it first loads, it will look up the routs and then select the component to load.
@NgModule({
    imports: [
        CommonModule,
        PeekModuleFactory.RouterModule,
        PeekModuleFactory.RouterModule.forChild(pluginRoutes),
        ...PeekModuleFactory.FormsModules,
    ],
    exports: [],
    providers: [
        TupleActionPushOfflineService, TupleActionPushService, {
            provide: TupleActionPushNameService,
            useFactory: tupleActionPushNameServiceFactory
        },
        TupleOfflineStorageService, {
            provide: TupleOfflineStorageNameService,
            useFactory: tupleOfflineStorageNameServiceFactory
        },
        TupleDataObserverService, TupleDataOfflineObserverService, {
            provide: TupleDataObservableNameService,
            useFactory: tupleDataObservableNameServiceFactory
        },
    ],
    declarations: [BranchComponent, BranchDetailComponent]
})
export class BranchModule {
}
