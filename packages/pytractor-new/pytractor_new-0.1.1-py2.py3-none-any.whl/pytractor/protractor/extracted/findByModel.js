try { return (function (model, using, rootSelector) {
  var root = document.querySelector(rootSelector || 'body');
  using = using || document;

  if (angular.getTestability) {
    return angular.getTestability(root).
        findModels(using, model, true);
  }
  var prefixes = ['ng-', 'ng_', 'data-ng-', 'x-ng-', 'ng\\:'];
  for (var p = 0; p < prefixes.length; ++p) {
    var selector = '[' + prefixes[p] + 'model="' + model + '"]';
    var elements = using.querySelectorAll(selector);
    if (elements.length) {
      return elements;
    }
  }
}).apply(this, arguments); }
catch(e) { throw (e instanceof Error) ? e : new Error(e); }