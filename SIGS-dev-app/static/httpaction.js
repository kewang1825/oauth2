  // import the module
import * as AdaptiveCards from "adaptivecards";

export class HttpAction extends AdaptiveCards.Action {
    method: string;
    body: string;
    signal: string;

    getJsonTypeName(): string {
        return "Action.Http";
    }

    execute() {
        ReactDOM.render(<ShowToken token={this.signal}/>, document.getElementById('token'));
    }

    parse(json: any, errors?: Array<AdaptiveCards.HostConfig.IValidationError>) {
        super.parse(json, errors);

        this.method = AdaptiveCards.getStringValue(json["method"]);
        this.body = AdaptiveCards.getStringValue(json["body"]);
        this.signal = AdaptiveCards.getStringValue(json["signal"]);
    }

    toJSON() : any {
        let result = super.toJSON();

        AdaptiveCards.setProperty(result, "method", this.method);
        AdaptiveCards.setProperty(result, "body", this.body);
        AdaptiveCards.setProperty(result, "signal", this.signal);

        return result;
    }
}

AdaptiveCards.AdaptiveCard.actionTypeRegistry.registerType("Action.Http", () => { return new HttpAction(); });
