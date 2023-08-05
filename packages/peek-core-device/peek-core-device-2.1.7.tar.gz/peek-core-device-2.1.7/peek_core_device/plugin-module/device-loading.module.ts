import {CommonModule} from "@angular/common";
import {NgModule} from "@angular/core";
import {LoadingComponent} from "peek_core_device/loading/loading.component";
import {PeekModuleFactory} from "@synerty/peek-util-web";


// Define the root module for this plugin.
// This module is loaded by the lazy loader, what ever this defines is what is started.
// When it first loads, it will look up the routs and then select the component to load.
@NgModule({
    imports: [
        CommonModule,
        ...PeekModuleFactory.FormsModules,
    ],
    exports: [LoadingComponent],
    providers: [
    ],
    declarations: [
        LoadingComponent,
    ]
})
export class DeviceLoadingModule {
}