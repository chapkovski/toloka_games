var hh;
var mm;
var parsedDate;
exports.Task = extend(
  TolokaHandlebarsTask,
  function (options) {
    TolokaHandlebarsTask.call(this, options);
  },
  {
    onRender: function () {
      try {

        const myd = $(this.getDOMElement());
        const fullDateText = myd.find('#fulltime').html();

        parsedDate = new Date(fullDateText + '+03:00')
        myd.find('#fulltime').html(parsedDate)

        myd.find('#hours_minutes').html(parsedDate.toLocaleTimeString())
        myd.find('#watch_time').html(parsedDate.toLocaleTimeString())
        whenReady(myd);
      }
      catch{}
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

const whenReady = (domik)=> {
const linkdiv = domik.find('#linkdiv');
const countcontainer = domik.find('#countcontainer');
var $clock = domik.find("#clock");
let date_to_set = parsedDate

if (new Date() > date_to_set) {
  console.debug('TOO LATE')
  linkdiv.removeClass("d-none");
  countcontainer.addClass("d-none");
}

const donecount = () => {
   linkdiv.removeClass("d-none");
  countcontainer.addClass("d-none");
};

  $clock.countdown(date_to_set, function (event) {
    $(this).html(event.strftime("%H:%M:%S"));
  }).on("finish.countdown", donecount)
  .on("stop.countdown", donecount)
  .countdown("start");
};