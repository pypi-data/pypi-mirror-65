// Error function
function memorize(target_url){
    nash.instance.load('target_url.xml').bind('target',{'url': target_url});
};

// Error function
function throwError(message){
    var error_display = nash.instance.load('_error_display.xml');
    error_display.bind('page.text',{'description': message})
    
    // var error_display = nash.instance.load('display.xml');
    // error_display.bind('choice',{'error': message})
    
    nash.record.stepsMgr().requestDone(nash.record.currentStepPosition());
    var target_url = "/record/" + nash.record.description().getRecordUid() + "/1/page/0";
    log.info('formUid = {} | target url = {} | message={}', nash.record.description().formUid, target_url, message);
    memorize(target_url);
} 

// All targets
var destination = {};

{%- for item in display.choice %}
destination['{{item.id}}'] = {};

{%- if 'target' in item %}
destination['{{item.id}}']['target'] = {{item.target|tojson}};
{%- endif -%}

{%- if 'nash_target' in item %}
destination['{{item.id}}']['nash_target'] = {{item.nash_target|tojson}};
{%- endif -%}

{%- if 'error_text' in item %}
destination['{{item.id}}']['error_text'] = {{item.error_text|tojson}};
{%- else %}
destination['{{item.id}}']['error_text'] = "La destination n'est pas définie.";
{%- endif -%}

{%- endfor %}

// test the length of the destination
if (destination.length == 0){
    return memorize("/");
}

if (_INPUT_.choice.selected == null) {
    var recordUid = nash.record.description().getRecordUid();
    log.info("No choice selected -> Redirection to the first page for the record {}", recordUid);
    return memorize("/record/" + recordUid + "/0/page/0");
}

// user choice from display
var choice = _INPUT_.choice.selected.id;

if (!(choice in destination)) { 
    log.error('formUid = {} | choice = {} | choice not in target', nash.record.description().formUid, choice);
    return throwError('Une erreur incompréhensible est survenue.'); 
};

var the_destination = destination[choice];
var target_url = "/"
if ('nash_target' in the_destination) {
    conf_target_url = _CONFIG_.get(the_destination['nash_target']+'.public.url');	
	if(conf_target_url == null){
        log.error('formUid = {} | nash_target = {} | nash_target doesn\'t exist', nash.record.description().formUid, the_destination['nash_target']);
        return throwError('La formalité cible est introuvable. La paramètre "nash_target" est incorrect.'); 
	}
    target_url = conf_target_url + "/";
}

if ('target' in the_destination) {
    target_url = target_url + "form/use?reference=" + encodeURIComponent(the_destination['target']);
} else {
    return throwError(the_destination['error_text']);
}

log.info('formUid = {} | choice = {} | target url = {}', nash.record.description().formUid, choice, target_url);

// redirect
return memorize(target_url);