class HttpAction extends AdaptiveCards.Action {

    get getJsonTypeName() {
        return "Action.Http";
    }

    execute() {
        const element = <h2>{this.signal}</h2>;
        ReactDOM.render(element, document.getElementById('signal'));

        var token = document.getElementById('token').innerText;
        $('#result').text('waiting...');
        $.post($SCRIPT_ROOT + '/postsignal?signal=' + this.signal + '&token=' + token, function(data) {
            $('#result').text(data);
        });
    }

    parse(json) {
        super.parse(json);

        this.signal = AdaptiveCards.getStringValue(json["signal"]);
    }

    get toJSON() {
        let result = super.toJSON();

        AdaptiveCards.setProperty(result, "signal", this.signal);
        return result;
    }
}

AdaptiveCards.AdaptiveCard.actionTypeRegistry.registerType("Action.Http", () => { return new HttpAction(); });
