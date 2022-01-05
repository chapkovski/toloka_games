exports.Task = extend(
  TolokaHandlebarsTask,
  function (options) {
    TolokaHandlebarsTask.call(this, options);
  },
  {
    onRender: function () {
      try {
        const assid = this.getAssignment().getId();
        const d = this.getDOMElement();
        const curhref = $(d).find("#assignmentlink").attr("href");
        const newUrl = assid
          ? curhref + "?participant_label=" + assid
          : curhref;
        $(d).find("#assignmentlink").attr("href", newUrl);
      } catch (e) {
        console.log(e);
      }
    },
  }
);

exports.TaskSuite = extend(
  TolokaHandlebarsTaskSuite,
  function (options) {
    TolokaHandlebarsTaskSuite.call(this, options);
  },
  { onRender: function () {} }
);

function extend(ParentClass, constructorFunction, prototypeHash) {
  constructorFunction = constructorFunction || function () {};
  prototypeHash = prototypeHash || {};
  if (ParentClass) {
    constructorFunction.prototype = Object.create(ParentClass.prototype);
  }
  for (var i in prototypeHash) {
    constructorFunction.prototype[i] = prototypeHash[i];
  }
  return constructorFunction;
}
