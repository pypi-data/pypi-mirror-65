import {CommonModule} from "@angular/common";
import {NgModule} from "@angular/core";
import {Routes} from "@angular/router";
// Import the default route component
import {CoreDeviceCfgComponent} from "./core-device-cfg.component";
import {ConnectComponent} from "./connect/connect.component";
// Import the required classes from VortexJS
import {
    TupleActionPushNameService,
    TupleActionPushOfflineService,
    TupleActionPushService,
    TupleDataObservableNameService,
    TupleDataObserverService,
    TupleDataOfflineObserverService,
    TupleOfflineStorageNameService,
    TupleOfflineStorageService
} from "@synerty/vortexjs";
// Import the names we need for the
import {
    deviceFilt,
    deviceObservableName,
    deviceTupleOfflineServiceName
} from "@peek/peek_core_device/_private/PluginNames";

// Import the names we need for the
import {deviceActionProcessorName} from "@peek/peek_core_device/_private";
import {PeekModuleFactory} from "@synerty/peek-util-web";

export function tupleActionPushNameServiceFactory() {
    return new TupleActionPushNameService(
        deviceActionProcessorName, deviceFilt);
}

export function tupleDataObservableNameServiceFactory() {
    return new TupleDataObservableNameService(
        deviceObservableName, deviceFilt);
}

export function tupleOfflineStorageNameServiceFactory() {
    return new TupleOfflineStorageNameService(deviceTupleOfflineServiceName);
}


// Define the child routes for this plugin
export const pluginRoutes: Routes = [
    // {
    //     path: 'showDiagram',
    //     component: CoreDeviceCfgComponent
    // },
    {
        path: '',
        pathMatch: 'full',
        component: CoreDeviceCfgComponent
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
        }
    ],
    declarations: [
        CoreDeviceCfgComponent,
        ConnectComponent
    ]
})
export class CoreDeviceCfgModule {
}
