/* Mystery Flower Box - storefront behaviour. No dependencies. */
(function () {
  "use strict";

  var money = function (cents) {
    var fmt = window.MFB && window.MFB.moneyFormat ? window.MFB.moneyFormat : "£{{amount}}";
    var amount = (cents / 100).toFixed(2);
    var withComma = amount.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return fmt.replace(/\{\{\s*amount\s*\}\}/, withComma)
              .replace(/\{\{\s*amount_no_decimals\s*\}\}/, Math.round(cents / 100))
              .replace(/\{\{\s*amount_with_comma_separator\s*\}\}/, amount.replace(".", ","));
  };

  /* ---------------------------------------------------------------- nav */
  document.addEventListener("click", function (e) {
    var toggle = e.target.closest("[data-nav-toggle]");
    if (!toggle) return;
    var nav = document.getElementById("mobile-nav");
    if (!nav) return;
    var open = nav.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  });

  /* ------------------------------------------------------- product media */
  document.addEventListener("click", function (e) {
    var thumb = e.target.closest("[data-media-thumb]");
    if (!thumb) return;
    var wrap = thumb.closest("[data-gallery]");
    if (!wrap) return;
    var main = wrap.querySelector("[data-media-main]");
    var src = thumb.getAttribute("data-src");
    var alt = thumb.getAttribute("data-alt") || "";
    if (main && src) { main.setAttribute("src", src); main.setAttribute("alt", alt); }
    wrap.querySelectorAll("[data-media-thumb]").forEach(function (t) {
      t.setAttribute("aria-current", t === thumb ? "true" : "false");
    });
  });

  /* --------------------------------------------------------- quantity */
  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-qty]");
    if (!btn) return;
    var input = btn.parentElement.querySelector("input");
    if (!input) return;
    var step = btn.getAttribute("data-qty") === "up" ? 1 : -1;
    var next = Math.max(parseInt(input.getAttribute("min") || "1", 10),
                        (parseInt(input.value, 10) || 1) + step);
    input.value = next;
    input.dispatchEvent(new Event("change", { bubbles: true }));
  });

  /* ----------------------------------------------------- the box builder */
  function BoxBuilder(root) {
    this.root = root;
    this.form = root.closest("form") || root.querySelector("form");
    this.summary = root.querySelector("[data-builder-summary]");
    this.surprise = root.querySelector("[data-full-surprise]");
    this.priceEl = document.querySelector("[data-product-price]");
    this.variantInput = root.querySelector("[data-variant-id]");
    this.variants = [];
    try { this.variants = JSON.parse(root.getAttribute("data-variants") || "[]"); } catch (err) {}
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
  };

  /* "Completely random / no clues" clears and locks every preference. */
  BoxBuilder.prototype.applySurprise = function () {
    var on = this.surprise && this.surprise.checked;
    this.root.querySelectorAll("[data-lockable]").forEach(function (group) {
      group.setAttribute("data-disabled", on ? "true" : "false");
      group.querySelectorAll("input, select").forEach(function (field) {
        if (field.hasAttribute("data-full-surprise")) return;
        if (on) {
          if (field.type === "checkbox" || field.type === "radio") field.checked = false;
          else if (field.tagName === "SELECT") field.selectedIndex = 0;
          field.setAttribute("disabled", "disabled");
        } else {
          field.removeAttribute("disabled");
        }
      });
    });
  };

  /* Keep at least some stems available: cap the number of exclusions. */
  BoxBuilder.prototype.limitExclusions = function (changed) {
    var group = changed.closest("[data-exclusion-group]");
    if (!group) return;
    var max = parseInt(group.getAttribute("data-max") || "0", 10);
    if (!max) return;
    var boxes = Array.prototype.slice.call(group.querySelectorAll("[data-exclusion]"));
    var checked = boxes.filter(function (b) { return b.checked; });
    var note = group.querySelector("[data-exclusion-note]");
    if (checked.length >= max) {
      boxes.forEach(function (b) { if (!b.checked) b.disabled = true; });
      if (note) note.hidden = false;
    } else {
      boxes.forEach(function (b) { b.disabled = false; });
      if (note) note.hidden = true;
    }
  };

  BoxBuilder.prototype.selectedVariant = function () {
    var chosen = this.root.querySelector("[data-purchase-option]:checked");
    var id = chosen ? chosen.value : (this.variants[0] && this.variants[0].id);
    return this.variants.filter(function (v) { return String(v.id) === String(id); })[0]
        || this.variants[0];
  };

  BoxBuilder.prototype.refresh = function () {
    var variant = this.selectedVariant();
    if (variant) {
      if (this.variantInput) this.variantInput.value = variant.id;
      if (this.priceEl) this.priceEl.textContent = money(variant.price);
      var perBox = document.querySelector("[data-price-per-box]");
      if (perBox && variant.boxes) {
        perBox.textContent = money(Math.round(variant.price / variant.boxes)) + " per box";
      } else if (perBox) {
        perBox.textContent = perBox.getAttribute("data-default") || "";
      }
      var btn = this.root.querySelector("[data-add-to-cart]");
      if (btn) {
        btn.disabled = !variant.available;
        var label = btn.querySelector("[data-add-label]");
        if (label) label.textContent = variant.available
          ? btn.getAttribute("data-label-default")
          : btn.getAttribute("data-label-sold-out");
      }
    }
    this.syncProperties();
    this.renderSummary();
  };

  /* Mirror the tick-boxes into the line item properties that reach the order. */
  BoxBuilder.prototype.syncProperties = function () {
    var self = this;
    ["colour", "variety", "care"].forEach(function (kind) {
      var target = self.root.querySelector("[data-property='" + kind + "']");
      if (!target) return;
      var values = self.collect("[data-exclusion][data-kind='" + kind + "']");
      target.value = values.join(", ");
    });
  };

  BoxBuilder.prototype.renderSummary = function () {
    if (!this.summary) return;
    var lines = [];
    if (this.surprise && this.surprise.checked) {
      lines.push("Total mystery — no clues, no exclusions. Bravest option. 🎁");
    } else {
      var colours = this.collect("[data-exclusion][data-kind='colour']");
      var varieties = this.collect("[data-exclusion][data-kind='variety']");
      var care = this.collect("[data-exclusion][data-kind='care']");
      var clue = this.root.querySelector("[data-clue]:checked");
      if (colours.length) lines.push("Leaving out these colours: " + colours.join(", "));
      if (varieties.length) lines.push("Leaving out these varieties: " + varieties.join(", "));
      if (care.length) lines.push("Household needs: " + care.join(", "));
      if (clue && clue.value && clue.value !== "No clue — total surprise") {
        lines.push("Clue before delivery: " + clue.value);
      }
      if (!lines.length) lines.push("No exclusions yet — you are open to anything. 🌷");
    }
    var date = this.root.querySelector("[data-delivery-date]");
    if (date && date.value) lines.push("Preferred delivery date: " + date.value);
    var gift = this.root.querySelector("[data-gift-message]");
    if (gift && gift.value.trim()) lines.push("Gift message included");

    this.summary.innerHTML = lines.map(function (l) {
      return "<li>" + l.replace(/[<>]/g, "") + "</li>";
    }).join("");
  };

  BoxBuilder.prototype.collect = function (selector) {
    return Array.prototype.slice.call(this.root.querySelectorAll(selector))
      .filter(function (i) { return i.checked; })
      .map(function (i) { return i.getAttribute("data-label") || i.value; });
  };

  document.querySelectorAll("[data-box-builder]").forEach(function (el) {
    new BoxBuilder(el);
  });

  /* Never send empty line item properties to the order. */
  document.addEventListener("submit", function (e) {
    var form = e.target;
    if (!form.querySelector || !form.querySelector("[data-box-builder], [data-variant-id]")) return;
    form.querySelectorAll("[name^='properties[']").forEach(function (field) {
      var empty = field.type === "checkbox" || field.type === "radio"
        ? !field.checked
        : !String(field.value || "").trim();
      if (empty) field.disabled = true;
    });
  }, true);

  /* --------------------------------------------------------------- tabs */
  document.querySelectorAll("[data-tabs]").forEach(function (group) {
    group.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-tab]");
      if (!btn) return;
      var key = btn.getAttribute("data-tab");
      group.querySelectorAll("[data-tab]").forEach(function (b) {
        b.setAttribute("aria-selected", b === btn ? "true" : "false");
      });
      var scope = document.querySelector(group.getAttribute("data-tabs")) || document;
      scope.querySelectorAll("[data-tab-panel]").forEach(function (panel) {
        var match = key === "all" || panel.getAttribute("data-tab-panel") === key;
        panel.hidden = !match;
      });
    });
  });

  /* ------------------------------------------------------------- filters */
  document.querySelectorAll("[data-filter-group]").forEach(function (group) {
    group.addEventListener("change", function () {
      var active = Array.prototype.slice.call(group.querySelectorAll("input:checked"))
        .map(function (i) { return i.value; });
      var targetSel = group.getAttribute("data-filter-group");
      document.querySelectorAll(targetSel + " [data-filter-tags]").forEach(function (card) {
        var tags = (card.getAttribute("data-filter-tags") || "").split("|");
        var show = !active.length || active.every(function (a) { return tags.indexOf(a) > -1; });
        card.hidden = !show;
      });
      var empty = document.querySelector(targetSel + " ~ [data-filter-empty]");
      if (empty) {
        var visible = document.querySelectorAll(targetSel + " [data-filter-tags]:not([hidden])").length;
        empty.hidden = visible > 0;
      }
    });
  });

  /* ------------------------------------------------------------- locator */
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
        items.forEach(function (i) {
          var hay = (i.getAttribute("data-search") || i.textContent).toLowerCase();
          i.hidden = q.length > 1 && hay.indexOf(q) === -1;
        });
      });
    }
  });

  /* ------------------------------------------------------- gallery likes */
  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-like]");
    if (!btn) return;
    var pressed = btn.getAttribute("aria-pressed") === "true";
    btn.setAttribute("aria-pressed", pressed ? "false" : "true");
    var count = btn.querySelector("[data-like-count]");
    if (count) {
      var n = parseInt(count.textContent, 10) || 0;
      count.textContent = pressed ? n - 1 : n + 1;
    }
    try {
      var key = "mfb-likes";
      var store = JSON.parse(localStorage.getItem(key) || "{}");
      var id = btn.getAttribute("data-like");
      if (pressed) { delete store[id]; } else { store[id] = 1; }
      localStorage.setItem(key, JSON.stringify(store));
    } catch (err) { /* private mode */ }
  });

  try {
    var likes = JSON.parse(localStorage.getItem("mfb-likes") || "{}");
    Object.keys(likes).forEach(function (id) {
      var btn = document.querySelector("[data-like='" + id + "']");
      if (btn && btn.getAttribute("aria-pressed") !== "true") btn.click();
    });
  } catch (err) { /* private mode */ }

  /* --------------------------------------------------------- copy to clip */
  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-copy]");
    if (!btn) return;
    var value = btn.getAttribute("data-copy");
    var done = function () {
      var original = btn.getAttribute("data-label") || btn.textContent;
      btn.setAttribute("data-label", original);
      btn.textContent = "Copied!";
      setTimeout(function () { btn.textContent = original; }, 1800);
    };
    if (navigator.clipboard) { navigator.clipboard.writeText(value).then(done, done); }
    else { done(); }
  });

  /* ------------------------------------------------------------ countdown */
  document.querySelectorAll("[data-countdown]").forEach(function (root) {
    var target = new Date(root.getAttribute("data-countdown")).getTime();
    if (isNaN(target)) return;
    var tick = function () {
      var diff = Math.max(0, target - Date.now());
      var d = Math.floor(diff / 86400000);
      var h = Math.floor(diff / 3600000) % 24;
      var m = Math.floor(diff / 60000) % 60;
      var s = Math.floor(diff / 1000) % 60;
      [["d", d], ["h", h], ["m", m], ["s", s]].forEach(function (pair) {
        var el = root.querySelector("[data-unit='" + pair[0] + "']");
        if (el) el.textContent = pair[1] < 10 ? "0" + pair[1] : pair[1];
      });
    };
    tick();
    setInterval(tick, 1000);
  });

  /* ------------------------------------------------- reveal on scroll */
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.style.opacity = "1";
          entry.target.style.transform = "none";
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    document.querySelectorAll("[data-reveal]").forEach(function (el) {
      el.style.opacity = "0";
      el.style.transform = "translateY(18px)";
      el.style.transition = "opacity .55s ease, transform .55s ease";
      io.observe(el);
    });
  }
})();
