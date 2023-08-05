// -*- coding: utf-8 -*-
// :Project:   SoL -- Show an animated countdown
// :Created:   mer 27 apr 2016 11:05:23 CEST
// :Author:    Lele Gaifax <lele@metapensiero.it>
// :License:   GNU General Public License version 3 or later
// :Copyright: © 2016 Lele Gaifax
//

//jsl:declare Audio
//jsl:declare clearInterval
//jsl:declare setInterval
//jsl:declare setTimeout
//jsl:declare soundManager

//////////////////
// IE polyfills //
//////////////////

Math.trunc = Math.trunc || function(x) {
  return x < 0 ? Math.ceil(x) : Math.floor(x);
};

///////////////////
// BaseCountdown //
///////////////////

function fullHeight(el) {
    return el.offsetHeight
        + parseInt(window.getComputedStyle(el).getPropertyValue('margin-top'))
        + parseInt(window.getComputedStyle(el).getPropertyValue('margin-bottom'));
}

function BaseCountdown(canvasId, duration, preAlarm, startedAt) {
    var title = document.getElementById('title'),
        buttons = document.getElementById('buttons'),
        wh = window.innerHeight - fullHeight(title) - fullHeight(buttons) - 20, // empirical
        ww = window.innerWidth - 20; // empirical

    this.duration = duration;
    this.preAlarm = preAlarm;
    if(Date.now() > (startedAt + 1000 * 60 * duration))
        startedAt = false;
    this.startedAt = startedAt;

    this.size = Math.min(wh, ww);
    this.lineWidth = Math.trunc(this.size / 30);
    this.radius = Math.trunc((this.size - this.lineWidth*1.1) / 2);
    this.squareSize = Math.trunc(Math.sqrt((this.radius*2) * (this.radius*2) / 2)
                                 - this.lineWidth);
    this.fontFamily = 'arial';
    this.fontSize = Math.trunc(this.squareSize / 2) + 'px';

    this.canvas = document.getElementById(canvasId);
    this.canvas.setAttribute("width", this.size);
    this.canvas.setAttribute("height", this.size);
    this.canvas.style.width = this.size + "px";
    this.canvas.style.height = this.size + "px";

    this.ctx = this.canvas.getContext("2d");
    this.ctx.font = this.fontSize + ' ' + this.fontFamily;
    this.ctx.lineWidth = this.lineWidth;
    this.ctx.strokeStyle = 'black';
    this.ctx.textBaseline = 'middle';
    this.ctx.textAlign = 'center';

    this.stopSign = document.getElementById('stop-sign');
    this.buttons = buttons;

    this.timeLeftTextHeight = null;
}

BaseCountdown.prototype.computeTextHeight = function(text, fontSize) {
    var self = this,
        div = document.createElement("div"),
        height;

    div.innerHTML = text;
    div.style.position = 'absolute';
    div.style.top = '-10000px';
    div.style.left = '-10000px';
    div.style.fontFamily = self.fontFamily;
    div.style.fontSize = fontSize || self.fontSize;
    document.body.appendChild(div);
    height = div.offsetHeight;
    document.body.removeChild(div);

    return height;
};

BaseCountdown.prototype.draw = function() {
    var self = this,
        middle = self.size / 2,
        ctx = self.ctx;

    ctx.clearRect(0, 0, self.size, self.size);

    ctx.beginPath();
    ctx.arc(middle, middle, self.radius, 0, 2 * Math.PI);
    ctx.stroke();
};

BaseCountdown.prototype.updateTimeLeft = function(left) {
    var self = this,
        ctx = self.ctx,
        mins = Math.trunc(left),
        secs = Math.trunc((left-mins)*60),
        mtext = mins + "'",
        stext = secs + '"',
        middle = self.size / 2,
        squareSize = self.squareSize,
        halfSquareSize = squareSize / 2,
        y;

    ctx.clearRect(middle - halfSquareSize, middle - halfSquareSize, squareSize, squareSize);

    if(!self.timeLeftTextHeight)
        self.timeLeftTextHeight = self.computeTextHeight(mtext);

    if(mins) {
        y = middle - self.timeLeftTextHeight / 2;
        ctx.fillText(mtext, middle, y);
        y += self.timeLeftTextHeight;
    } else {
        y = middle;
    }
    ctx.fillText(stext, middle, y);
};

BaseCountdown.prototype.drawInterval = function() {
    var self = this,
        fontSize = self.radius / 10 + 'px',
        textHeight = self.computeTextHeight('1', fontSize),
        radius = self.radius * 0.9 - textHeight / 2,
        ctx = self.ctx,
        middle = self.size / 2,
        start = new Date(self.startedAt),
        stop = new Date(self.startedAt + 1000 * 60 * self.duration),
        lpad = function(num) {
            return (num < 10 ? '0' : '') + num;
        },
        textRadiants = function(t) {
            var angle = 0;
            for (var i = t.length-1; i >= 0; i--) {
                var cw = ctx.measureText(text[i]).width;
                angle += (cw / (radius - textHeight));
            }
            return angle;
        },
        drawCurvedText = function(t, top) {
            var angle;

            ctx.save();
            ctx.font = fontSize + ' ' + self.fontFamily;
            ctx.lineCap = "round";
            ctx.lineWidth = self.lineWidth / 10;
            ctx.translate(middle, middle);

            angle = (top ? -1 : 1) * textRadiants(t) / 2;
            ctx.rotate(angle);

            for (var i = 0; i < t.length; i++) {
                var cw = ctx.measureText(t[i]).width,
                    ca = cw / (radius - textHeight);
                ctx.rotate((top ? 1 : -1) * ca / 2);
                if(t[i] == '—') {
                    var sep = (top ? -1 : 1) * Math.PI / 2 + (top ? 1 : -1) * angle;
                    ctx.beginPath();
                    ctx.arc(0, 0, radius + textHeight / 2, sep, sep + ca);
                    ctx.stroke();
                } else
                    ctx.fillText(t[i], 0, (top ? -1 : 1) * (radius + textHeight / 2));
                ctx.rotate((top ? 1 : -1) * ca / 2);
                angle += (top ? 1 : -1) * ca;
            }
            ctx.restore();
        }, text;

    text = lpad(start.getHours())
        + ':'
        + lpad(start.getMinutes())
        + ':'
        + lpad(start.getSeconds())
        + ' — '
        + lpad(stop.getHours())
        + ':'
        + lpad(stop.getMinutes())
        + ':'
        + lpad(stop.getSeconds());
    drawCurvedText(text, true);
    // drawCurvedText(text, false);
};

BaseCountdown.prototype.stop = function() {
    var self = this;

    if(self.updateInterval) {
        clearInterval(self.updateInterval);
        self.updateInterval = 0;
    }
};

BaseCountdown.prototype.terminate = function() {
    var self = this,
        canvas = self.canvas,
        stopSign = self.stopSign,
        buttons = self.buttons,
        right = false;

    self.stop();

    canvas.classList.toggle('invisible');
    stopSign.classList.toggle('invisible');
    buttons.classList.toggle('invisible');

    function swing() {
        stopSign.classList[right ? 'remove' : 'add']('swing-right');
        stopSign.classList[right ? 'add' : 'remove']('swing-left');
        right = !right;
        setTimeout(swing, 1000);
    }

    setTimeout(swing, 500);
};

BaseCountdown.prototype.close = function() {
    var self = this;

    self.stop();
    window.close();
};

//////////////////
// PreCountdown //
//////////////////

function PreCountdown(canvasId, duration, preAlarm) {
    Countdown.call(this, canvasId, duration, preAlarm);
    this.pre_alarm_done = false;
}

PreCountdown.prototype = Object.create(BaseCountdown.prototype);

PreCountdown.prototype.addMinutes = function(minutes) {
    var self = this;

    self.duration += minutes;
    self.pre_alarm_done = false;
    self.draw();
    self.drawInterval();
};

PreCountdown.prototype.start = function() {
    var self = this,
        ctx = self.ctx,
        middle = self.size/2,
        radius = self.radius,
        start = -Math.PI / 2;

    function update() {
        var started_at = self.startedAt,
            now = Date.now(),
            total_ticks = 1000 * 60 * self.duration,
            radiants_per_tick = 2 * Math.PI / total_ticks,
            progress = now - started_at,
            pre_alarm = (self.preAlarm
                         ? started_at + 1000 * 60 * (self.duration - self.preAlarm)
                         : false);

        ctx.beginPath();
        ctx.arc(middle, middle, radius, 0, 2 * Math.PI);
        ctx.stroke();

        start = 2*Math.PI * progress / 1000 / 60 - Math.PI / 2;

        ctx.save();
        ctx.beginPath();
        ctx.strokeStyle = !pre_alarm || now > pre_alarm ? 'red' : 'orange';
        ctx.lineWidth = self.lineWidth * 0.9;
        ctx.arc(middle, middle, radius, start, start + progress * radiants_per_tick);
        ctx.stroke();
        ctx.restore();

        if(progress < total_ticks) {
            if(!self.pre_alarm_done && pre_alarm && now > pre_alarm) {
                soundManager.play('prealarm');
                self.pre_alarm_done = true;
            }
            self.updateTimeLeft(self.duration - (progress / 1000 / 60));
        } else {
            self.stop();
            soundManager.play('stop');
            self.terminate();
        }
    }

    self.startedAt = Date.now();
    self.drawInterval();
    self.updateInterval = setInterval(update, 1000/20);
};

///////////////
// Countdown //
///////////////

function Countdown(canvasId, duration, preAlarm, startedAt, isowner) {
    BaseCountdown.call(this, canvasId, duration, preAlarm, startedAt);

    this.isowner = isowner;

    this.updateInterval = 0;
    this.tictacting = false;
}

Countdown.prototype = Object.create(BaseCountdown.prototype);

Countdown.prototype.draw = function(noimage) {
    var self = this,
        scr = document.getElementById('scr'),
        middle = self.size / 2,
        ih = self.squareSize,
        iw = self.squareSize * (scr.width / scr.height),
        ctx = self.ctx;

    BaseCountdown.prototype.draw.call(self);

    if(self.startedAt)
        self.start();
    else
        if(!noimage)
            ctx.drawImage(scr, middle - iw / 2, middle - ih / 2,  iw, ih);
};

Countdown.prototype.stop = function() {
    var self = this;

    BaseCountdown.prototype.stop.call(self);

    self.startedAt = false;

    if(self.tictacting) {
        soundManager.stop('tictac');
        self.tictacting = false;
    }

    if(self.isowner) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", self.notifyStart, false);
        xhr.send();
    }
};

Countdown.prototype.close = function() {
    var self = this;

    if(self.updateInterval) {
        if(!window.confirm(self.confirmClose))
            return;

        self.stop();
    }
    window.close();
};

Countdown.prototype.start = function(delay_secs) {
    var self = this;

    if(self.updateInterval) {
        if(!window.confirm(self.confirmRestart))
            return;

        self.stop();
        self.draw(true);
    }

    var ctx = self.ctx,
        middle = self.size/2,
        radius = self.radius,
        start = -Math.PI / 2,
        total_ticks = 1000 * (delay_secs || (60 * self.duration)),
        radiants_per_tick = 2 * Math.PI / total_ticks,
        half_game, pre_alarm, last_minute,
        pre_alarm_done = false;

    self.tictacting = false;

    function update() {
        var now = Date.now(),
            progress = now - self.startedAt;

        ctx.beginPath();
        ctx.arc(middle, middle, radius, start-0.1, start + progress * radiants_per_tick);
        ctx.stroke();

        start = 2*Math.PI * progress / 1000 / 60 - Math.PI / 2;

        ctx.save();
        ctx.beginPath();
        ctx.lineWidth = self.lineWidth * 0.9;
        if(delay_secs)
            ctx.strokeStyle = 'red';
        else
            ctx.strokeStyle = (pre_alarm && now > pre_alarm
                               ? 'red'
                               : (now > half_game
                                  ? 'orange'
                                  : 'yellow'));
        ctx.arc(middle, middle, radius, start, start + progress * radiants_per_tick);
        ctx.stroke();
        ctx.restore();

        if(progress < total_ticks) {
            if(!pre_alarm_done && pre_alarm && now > pre_alarm) {
                soundManager.play('prealarm');
                pre_alarm_done = true;
            }
            if(!self.tictacting && now > last_minute) {
                soundManager.play('tictac', { loops: 60 });
                self.tictacting = true;
            }
            self.updateTimeLeft((delay_secs ? delay_secs / 60 : self.duration)
                                - (progress / 1000 / 60));
        } else {
            self.stop();
            if(delay_secs) {
                self.draw(true);
                self.start();
            } else {
                soundManager.play('stop');
                self.terminate();
            }
        }
    }

    if(!self.startedAt) {
        self.startedAt = Date.now();
        if(delay_secs) {
            self.tictacting = true;
            soundManager.play('tictac', { loops: delay_secs });
        } else {
            soundManager.play('start');
            if(self.isowner) {
                var xhr = new XMLHttpRequest();
                xhr.open("POST", self.notifyStart + '&start=' + self.startedAt, true);
                xhr.send();
            }
        }
    }

    half_game = self.startedAt + 1000 * 30 * self.duration;
    if(self.preAlarm) {
        pre_alarm = self.startedAt + 1000 * 60 * (self.duration - self.preAlarm);
        pre_alarm_done = Date.now() > pre_alarm;
    } else
        pre_alarm = false;
    last_minute = self.startedAt + 1000 * 60 * (self.duration - 1);

    self.drawInterval();
    self.updateInterval = setInterval(update, 1000/20);
};
