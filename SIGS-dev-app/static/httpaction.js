function GetHttp(url) {
    $('#result').text('waiting...');
    $.getJSON(url, null, function(data) {
        $('#result').text(JSON.stringify(data, null, 2));
    });
}

function OpenHttp(url) {
    window.open(url, "_blank");
}

// Extends a new action type: Action.Http
class HttpAction extends AdaptiveCards.Action {

    get getJsonTypeName() {
        return 'Action.Http';
    }

    execute() {
        if (this.url != null) {
            if (this.method == "GET") {
                GetHttp(this.url);
            } else {
                OpenHttp(this.url);
            }
        }

        // Check if signal is set, then post the signal after the action is performed
        RenderAndPostSignal(this.signal);
    }

    parse(json) {
        super.parse(json);

        this.method = AdaptiveCards.getStringValue(json["method"]);
        this.url = AdaptiveCards.getStringValue(json["url"]);
        this.signal = AdaptiveCards.getStringValue(json["signal"]);
    }

    get toJSON() {
        let result = super.toJSON();

        AdaptiveCards.setProperty(result, "method", this.method);
        AdaptiveCards.setProperty(result, "url", this.url);
        AdaptiveCards.setProperty(result, "signal", this.signal);
        return result;
    }
}

AdaptiveCards.AdaptiveCard.actionTypeRegistry.registerType("Action.Http", () => { return new HttpAction(); });
