# Something New

+ Override the values in Request Object
    + values: ARGS+FORM+JSON
+ Add werkzeug.utils.validate_arguments() in dispatch_request
    + if arguments list not match, raise BadRequest()
