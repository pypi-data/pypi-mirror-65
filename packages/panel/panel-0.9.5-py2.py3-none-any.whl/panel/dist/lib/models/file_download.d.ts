import { InputWidget, InputWidgetView } from "@bokehjs/models/widgets/input_widget";
import { ButtonType } from "@bokehjs/core/enums";
import * as p from "@bokehjs/core/properties";
export declare class FileDownloadView extends InputWidgetView {
    model: FileDownload;
    anchor_el: HTMLAnchorElement;
    _initialized: boolean;
    connect_signals(): void;
    render(): void;
    _update_label(): void;
    click(): void;
}
export declare namespace FileDownload {
    type Attrs = p.AttrsOf<Props>;
    type Props = InputWidget.Props & {
        auto: p.Property<boolean>;
        button_type: p.Property<ButtonType>;
        clicks: p.Property<number>;
        data: p.Property<string | null>;
        label: p.Property<string>;
        filename: p.Property<string | null>;
    };
}
export interface FileDownload extends FileDownload.Attrs {
}
export declare class FileDownload extends InputWidget {
    properties: FileDownload.Props;
    constructor(attrs?: Partial<FileDownload.Attrs>);
    static __module__: string;
    static init_FileDownload(): void;
}
