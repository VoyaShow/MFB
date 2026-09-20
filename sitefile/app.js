/* Mystery Flower Box — single-file storefront prototype.
   Routing works without JavaScript (CSS :target). Everything here is
   enhancement: the box builder, the basket, filters and form handling. */
(function () {
  "use strict";

  var HOME = "home";
  var money = function (p) { return "£" + p.toFixed(2); };

  /* ------------------------------------------------------------- routing */
  function pageIdFromHash() {
    var h = (location.hash || "").replace(/^#/, "");
    if (!h) return HOME;
    return document.getElementById(h) ? h : h;
  }

  function showPage(id, push) {
    var target = document.getElementById(id);
    if (!target || !target.classList.contains("page")) {
      target = document.getElementById("not-found") || document.getElementById(HOME);
      id = target.id;
    }
    document.querySelectorAll(".page").forEach(function (p) {
      p.classList.toggle("is-active", p === target);
    });
    document.title = (target.getAttribute("data-title") || "Mystery Flower Box") +
      " — Mystery Flower Box";
    closeNav();
    if (push !== false) window.scrollTo({ top: 0, behavior: "instant" in window ? "auto" : "auto" });
  }

  function route() { showPage(pageIdFromHash()); }
  window.addEventListener("hashchange", route);

  /* In-page anchors (e.g. #quote) should scroll, not switch page. */
  document.addEventListener("click", function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a) return;
    var id = a.getAttribute("href").slice(1);
    var el = document.getElementById(id);
    if (el && !el.classList.contains("page")) {
      e.preventDefault();
      el.scrollIntoView({ behavior: "smooth", block: "start" });
      closeNav();
    }
  });

  /* ------------------------------------------------------------ mobile nav */
  function closeNav() {
    var nav = document.getElementById("mobile-nav");
    if (nav) nav.classList.remove("is-open");
    var t = document.querySelector("[data-nav-toggle]");
    if (t) t.setAttribute("aria-expanded", "false");
  }

  document.addEventListener("click", function (e) {
    var toggle = e.target.closest("[data-nav-toggle]");
    if (!toggle) return;
    var nav = document.getElementById("mobile-nav");
    if (!nav) return;
    var open = nav.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  });

  /* ---------------------------------------------------------- product art */
  document.addEventListener("click", function (e) {
    var thumb = e.target.closest("[data-art-thumb]");
    if (!thumb) return;
    var wrap = thumb.closest("[data-gallery]");
    var main = wrap && wrap.querySelector("[data-art-main] use");
    if (main) {
      main.setAttribute("href", "#" + thumb.getAttribute("data-art-thumb"));
      main.setAttribute("xlink:href", "#" + thumb.getAttribute("data-art-thumb"));
    }
    wrap.querySelectorAll("[data-art-thumb]").forEach(function (t) {
      t.setAttribute("aria-current", t === thumb ? "true" : "false");
    });
  });

  /* -------------------------------------------------------------- quantity */
  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-qty]");
    if (!btn) return;
    var input = btn.parentElement.querySelector("input");
    if (!input) return;
    var step = btn.getAttribute("data-qty") === "up" ? 1 : -1;
    var min = parseInt(input.getAttribute("min") || "1", 10);
    input.value = Math.max(min, (parseInt(input.value, 10) || 1) + step);
    input.dispatchEvent(new Event("change", { bubbles: true }));
  });

  /* ---------------------------------------------------------- the basket */
  var BASKET_KEY = "mfb-basket";

  function readBasket() {
    try { return JSON.parse(localStorage.getItem(BASKET_KEY) || "[]"); }
    catch (err) { return window.__mfbBasket || []; }
  }
  function writeBasket(items) {
    window.__mfbBasket = items;
    try { localStorage.setItem(BASKET_KEY, JSON.stringify(items)); } catch (err) {}
    renderBasket();
  }

  function basketCount() {
    return readBasket().reduce(function (n, i) { return n + i.qty; }, 0);
  }
  function basketTotal() {
    return readBasket().reduce(function (n, i) { return n + i.price * i.qty; }, 0);
  }

  function renderBasket() {
    var count = basketCount();
    document.querySelectorAll("[data-basket-count]").forEach(function (el) {
      el.textContent = count;
      el.hidden = count === 0;
    });

    var list = document.querySelector("[data-basket-list]");
    if (!list) return;
    var items = readBasket();
    var empty = document.querySelector("[data-basket-empty]");
    var filled = document.querySelector("[data-basket-filled]");
    if (empty) empty.hidden = items.length > 0;
    if (filled) filled.hidden = items.length === 0;

    list.innerHTML = items.map(function (item, index) {
      var props = (item.props || []).map(function (p) {
        return "<li><strong>" + esc(p[0]) + ":</strong> " + esc(p[1]) + "</li>";
      }).join("");
      return '<div class="basket-line">' +
        '<div class="basket-line__art"><svg class="art art--square" viewBox="0 0 1400 1400" role="img" aria-label="' +
          esc(item.title) + '"><use href="#' + esc(item.art) + '" xlink:href="#' + esc(item.art) + '"/></svg></div>' +
        '<div class="basket-line__body">' +
          '<div class="basket-line__title">' + esc(item.title) + '</div>' +
          '<div class="muted small">' + esc(item.plan) + " · " + money(item.price) + " each</div>" +
          (props ? '<ul class="basket-line__props">' + props + "</ul>" : "") +
          '<div class="cluster" style="margin-top:10px">' +
            '<div class="quantity"><button type="button" data-qty="down" aria-label="Decrease">&minus;</button>' +
            '<input type="number" min="1" value="' + item.qty + '" data-basket-qty="' + index + '" aria-label="Quantity"></input>' +
            '<button type="button" data-qty="up" aria-label="Increase">+</button></div>' +
            '<button class="basket-line__remove" type="button" data-basket-remove="' + index + '">Remove</button>' +
          "</div>" +
        "</div>" +
        '<div class="basket-line__price">' + money(item.price * item.qty) + "</div>" +
        "</div>";
    }).join("");

    var total = document.querySelector("[data-basket-total]");
    if (total) total.textContent = money(basketTotal());
  }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  document.addEventListener("change", function (e) {
    var q = e.target.closest("[data-basket-qty]");
    if (!q) return;
    var items = readBasket();
    var i = parseInt(q.getAttribute("data-basket-qty"), 10);
    if (items[i]) { items[i].qty = Math.max(1, parseInt(q.value, 10) || 1); writeBasket(items); }
  });

  document.addEventListener("click", function (e) {
    var r = e.target.closest("[data-basket-remove]");
    if (!r) return;
    var items = readBasket();
    items.splice(parseInt(r.getAttribute("data-basket-remove"), 10), 1);
    writeBasket(items);
    toast("Removed from your basket");
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest("[data-basket-clear]")) return;
    writeBasket([]);
    toast("Basket emptied");
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest("[data-checkout]")) return;
    toast("This is a preview — checkout opens on the real store");
  });

  /* ---------------------------------------------------------------- toast */
  var toastEl;
  function toast(message) {
    if (!toastEl) {
      toastEl = document.createElement("div");
      toastEl.className = "toast";
      toastEl.setAttribute("role", "status");
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = message;
    requestAnimationFrame(function () { toastEl.classList.add("is-up"); });
    clearTimeout(toastEl._t);
    toastEl._t = setTimeout(function () { toastEl.classList.remove("is-up"); }, 2600);
  }

  /* --------------------------------------------------------- box builder */
  function BoxBuilder(root) {
    this.root = root;
    this.summary = root.querySelector("[data-builder-summary]");
    this.surprise = root.querySelector("[data-full-surprise]");
    var scope = root.closest(".page") || document;
    this.priceEl = scope.querySelector("[data-product-price]");
    this.perBoxEl = scope.querySelector("[data-price-per-box]");
    this.plans = JSON.parse(root.getAttribute("data-plans"));
    this.title = root.getAttribute("data-title");
    this.art = root.getAttribute("data-art");
    this.bind();
    this.refresh();
  }

  BoxBuilder.prototype.bind = function () {
    var self = this;
    this.root.addEventListener("change", function (e) {
      if (e.target.matches("[data-full-surprise]")) self.applySurprise();
      if (e.target.matches("[data-exclusion]")) self.limitExclusions(e.target);
      self.refresh();
    });
    this.root.addEventListener("submit", function (e) {
      e.preventDefault();
      self.addToBasket();
    });
  };

  /* "Total mystery" clears and locks every preference below it. */
  BoxBuilder.prototype.applySurprise = function () {
    var on = this.surprise && this.surprise.checked;
    this.root.querySelectorAll("[data-lockable]").forEach(function (group) {
      group.setAttribute("data-disabled", on ? "true" : "false");
      group.querySelectorAll("input, select").forEach(function (field) {
        if (on) {
          if (field.type === "checkbox") field.checked = false;
          else if (field.type === "radio") field.checked = field.hasAttribute("data-default");
          field.disabled = true;
        } else {
          field.disabled = false;
        }
      });
      var note = group.querySelector("[data-exclusion-note]");
      if (note) note.hidden = true;
    });
  };

  /* Keep enough stems to fill a box: cap how much can be excluded. */
  BoxBuilder.prototype.limitExclusions = function (changed) {
    var group = changed.closest("[data-exclusion-group]");
    if (!group) return;
    var max = parseInt(group.getAttribute("data-max") || "0", 10);
    if (!max) return;
    var boxes = Array.prototype.slice.call(group.querySelectorAll("[data-exclusion]"));
    var chosen = boxes.filter(function (b) { return b.checked; });
    var note = group.querySelector("[data-exclusion-note]");
    boxes.forEach(function (b) { if (!b.checked) b.disabled = chosen.length >= max; });
    if (note) note.hidden = chosen.length < max;
  };

  BoxBuilder.prototype.plan = function () {
    var chosen = this.root.querySelector("[data-plan]:checked");
    var key = chosen ? chosen.value : this.plans[0].id;
    for (var i = 0; i < this.plans.length; i++) {
      if (this.plans[i].id === key) return this.plans[i];
    }
    return this.plans[0];
  };

  BoxBuilder.prototype.collect = function (kind) {
    return Array.prototype.slice.call(
      this.root.querySelectorAll("[data-exclusion][data-kind='" + kind + "']"))
      .filter(function (i) { return i.checked; })
      .map(function (i) { return i.value; });
  };

  BoxBuilder.prototype.properties = function () {
    var out = [];
    if (this.surprise && this.surprise.checked) {
      out.push(["Mystery level", "Total mystery — no clues, no exclusions"]);
    } else {
      var colours = this.collect("colour");
      var varieties = this.collect("variety");
      var care = this.collect("care");
      if (colours.length) out.push(["Flower colours to leave out", colours.join(", ")]);
      if (varieties.length) out.push(["Flower varieties to leave out", varieties.join(", ")]);
      if (care.length) out.push(["Household needs", care.join(", ")]);
      var clue = this.root.querySelector("[data-clue]:checked");
      if (clue && !clue.hasAttribute("data-default")) {
        out.push(["Clue before delivery", clue.value]);
      }
    }
    var date = this.root.querySelector("[data-delivery-date]");
    if (date && date.value) out.push(["Preferred delivery date", date.value]);
    var gift = this.root.querySelector("[data-gift-message]");
    if (gift && gift.value.trim()) out.push(["Gift message", gift.value.trim()]);
    return out;
  };

  BoxBuilder.prototype.refresh = function () {
    var plan = this.plan();
    if (this.priceEl) this.priceEl.textContent = money(plan.price);
    if (this.perBoxEl) {
      this.perBoxEl.textContent = plan.boxes > 1
        ? money(plan.price / plan.boxes) + " per box · free UK delivery"
        : "One clear price · free UK delivery";
    }
    var btn = this.root.querySelector("[data-add]");
    if (btn) btn.textContent = "Add my surprise — " + money(plan.price);

    if (this.summary) {
      var props = this.properties();
      var lines = props.map(function (p) {
        return "<li><strong>" + esc(p[0]) + ":</strong> " + esc(p[1]) + "</li>";
      });
      if (!lines.length) {
        lines = ["<li>No exclusions yet — you are open to anything. 🌷</li>"];
      }
      this.summary.innerHTML = lines.join("");
    }
  };

  BoxBuilder.prototype.addToBasket = function () {
    var plan = this.plan();
    var qtyInput = this.root.querySelector("[data-builder-qty]");
    var qty = Math.max(1, parseInt(qtyInput && qtyInput.value, 10) || 1);
    var items = readBasket();
    items.push({
      title: this.title,
      art: this.art,
      plan: plan.label,
      price: plan.price,
      qty: qty,
      props: this.properties()
    });
    writeBasket(items);
    toast("Added to your basket 🌸");
  };

  /* ------------------------------------------------------------ tab filters */
  document.querySelectorAll("[data-tabs]").forEach(function (group) {
    group.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-tab]");
      if (!btn) return;
      var key = btn.getAttribute("data-tab");
      group.querySelectorAll("[data-tab]").forEach(function (b) {
        b.setAttribute("aria-selected", b === btn ? "true" : "false");
      });
      var scope = document.querySelector(group.getAttribute("data-tabs"));
      if (!scope) return;
      scope.querySelectorAll("[data-tab-panel]").forEach(function (panel) {
        panel.hidden = key !== "all" && panel.getAttribute("data-tab-panel") !== key;
      });
    });
  });

  /* ---------------------------------------------------------------- locator */
  document.querySelectorAll("[data-locator]").forEach(function (root) {
    var search = root.querySelector("[data-locator-search]");
    var items = Array.prototype.slice.call(root.querySelectorAll("[data-locator-item]"));
    var pins = Array.prototype.slice.call(root.querySelectorAll("[data-locator-pin]"));

    function focus(key) {
      items.forEach(function (i) {
        i.setAttribute("aria-current", i.getAttribute("data-locator-item") === key ? "true" : "false");
      });
      pins.forEach(function (p) {
        p.setAttribute("aria-current", p.getAttribute("data-locator-pin") === key ? "true" : "false");
      });
      var el = root.querySelector("[data-locator-item='" + key + "']");
      if (el) el.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }

    root.addEventListener("click", function (e) {
      var item = e.target.closest("[data-locator-item]");
      if (item) return focus(item.getAttribute("data-locator-item"));
      var pin = e.target.closest("[data-locator-pin]");
      if (pin) return focus(pin.getAttribute("data-locator-pin"));
    });

    if (search) {
      search.addEventListener("input", function () {
        var q = search.value.trim().toLowerCase();
        var shown = 0;
        items.forEach(function (i) {
          var hit = q.length < 2 || i.getAttribute("data-search").toLowerCase().indexOf(q) > -1;
          i.hidden = !hit;
          if (hit) shown++;
        });
        var none = root.querySelector("[data-locator-none]");
        if (none) none.hidden = shown > 0;
      });
    }
  });

  /* ------------------------------------------------------------ gallery likes */
  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-like]");
    if (!btn) return;
    var pressed = btn.getAttribute("aria-pressed") === "true";
    btn.setAttribute("aria-pressed", pressed ? "false" : "true");
    var count = btn.querySelector("[data-like-count]");
    if (count) {
      var n = parseInt(String(count.textContent).replace(/,/g, ""), 10) || 0;
      count.textContent = (pressed ? n - 1 : n + 1).toLocaleString("en-GB");
    }
  });

  /* ---------------------------------------------------------------- copying */
  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-copy]");
    if (!btn) return;
    var value = btn.getAttribute("data-copy");
    if (navigator.clipboard) navigator.clipboard.writeText(value).catch(function () {});
    toast("Copied: " + value);
  });

  /* ------------------------------------------------------------------ forms */
  document.addEventListener("submit", function (e) {
    var form = e.target.closest("[data-demo-form]");
    if (!form) return;
    e.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    var done = form.querySelector("[data-form-success]");
    var fields = form.querySelector("[data-form-fields]");
    if (done) done.hidden = false;
    if (fields) fields.hidden = true;
    if (done) done.scrollIntoView({ behavior: "smooth", block: "center" });
  });

  /* -------------------------------------------------------------- countdown */
  document.querySelectorAll("[data-countdown]").forEach(function (root) {
    var target = new Date(root.getAttribute("data-countdown")).getTime();
    if (isNaN(target)) return;
    function tick() {
      var diff = Math.max(0, target - Date.now());
      var parts = {
        d: Math.floor(diff / 86400000),
        h: Math.floor(diff / 3600000) % 24,
        m: Math.floor(diff / 60000) % 60,
        s: Math.floor(diff / 1000) % 60
      };
      Object.keys(parts).forEach(function (k) {
        var el = root.querySelector("[data-unit='" + k + "']");
        if (el) el.textContent = parts[k] < 10 ? "0" + parts[k] : parts[k];
      });
    }
    tick();
    setInterval(tick, 1000);
  });

  /* --------------------------------------------------------------- reveal in */
  function reveal(el) {
    el.style.opacity = "1";
    el.style.transform = "none";
  }

  if ("IntersectionObserver" in window &&
      !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        reveal(entry.target);
        io.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -6% 0px" });
    document.querySelectorAll("[data-reveal]").forEach(function (el) {
      el.style.opacity = "0";
      el.style.transform = "translateY(16px)";
      el.style.transition = "opacity .5s ease, transform .5s ease";
      io.observe(el);
    });
    /* Failsafe: nothing should ever stay invisible, whatever the viewer does. */
    setTimeout(function () {
      document.querySelectorAll("[data-reveal]").forEach(reveal);
    }, 4000);
    window.addEventListener("hashchange", function () {
      setTimeout(function () {
        document.querySelectorAll(".page.is-active [data-reveal]").forEach(function (el) {
          if (el.getBoundingClientRect().top < window.innerHeight) reveal(el);
        });
      }, 60);
    });
  }

  /* ------------------------------------------------------------------- boot */
  document.querySelectorAll("[data-box-builder]").forEach(function (el) { new BoxBuilder(el); });
  renderBasket();
  route();
})();
