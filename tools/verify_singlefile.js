/* Drives the built single-file storefront in a real browser: renders every
   page, exercises the box builder, basket, gallery filters, locator and forms,
   and screenshots desktop and mobile.

   Usage:  npm i -D playwright && node tools/verify_singlefile.js            */
const { chromium } = require('playwright');
const path = require('path');
const SHOTS = process.env.SHOTS_DIR || path.resolve(__dirname, '..', 'dist', 'shots');
const FILE = 'file://' + path.resolve(__dirname, '..', 'dist', 'mystery-flower-box.html');
require('fs').mkdirSync(SHOTS, { recursive: true });

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || undefined, args: ['--no-sandbox'] });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));

  await page.goto(FILE, { waitUntil: 'load' });
  await page.waitForTimeout(400);

  const ids = await page.$$eval('.page', els => els.map(e => e.id));
  console.log('pages found:', ids.length);

  const bad = [];
  for (const id of ids) {
    await page.goto(FILE + '#' + id, { waitUntil: 'load' });
    await page.waitForTimeout(120);
    const info = await page.evaluate((pid) => {
      const el = document.getElementById(pid);
      const visible = el && el.offsetParent !== null && el.getBoundingClientRect().height > 100;
      const others = Array.from(document.querySelectorAll('.page'))
        .filter(p => p.id !== pid && p.offsetParent !== null).map(p => p.id);
      return { visible, others, h: el ? Math.round(el.getBoundingClientRect().height) : 0,
               title: document.title };
    }, id);
    if (!info.visible || info.others.length) bad.push({ id, ...info });
  }
  console.log('pages that failed to render alone:', bad.length ? JSON.stringify(bad) : 'none');

  // --- box builder ---------------------------------------------------------
  await page.goto(FILE + '#mystery-flower-box', { waitUntil: 'load' });
  await page.waitForTimeout(200);
  await page.click('#mystery-flower-box-col-0 + label');   // Red
  await page.click('#mystery-flower-box-col-2 + label');   // Orange
  await page.click('#mystery-flower-box-col-5 + label');   // Purple
  const capped = await page.$eval('#mystery-flower-box-col-1', e => e.disabled);
  const noteShown = await page.$eval('#mystery-flower-box [data-exclusion-group] [data-exclusion-note]',
                                     e => !e.hidden);
  await page.click('#mystery-flower-box-var-1 + label');   // Lilies
  await page.click('#mystery-flower-box-care-0 + label');  // Pet-friendly
  const summary = await page.$eval('#mystery-flower-box [data-builder-summary]', e => e.innerText);
  console.log('exclusion cap at 3 colours:', capped, '| cap note shown:', noteShown);
  console.log('summary:\n' + summary.split('\n').map(s => '   ' + s).join('\n'));

  // plan switch updates price
  await page.click('label[for="plan-mystery-flower-box-four"]');
  const price = await page.$eval('#mystery-flower-box [data-product-price]', e => e.textContent);
  const perBox = await page.$eval('#mystery-flower-box [data-price-per-box]', e => e.textContent);
  console.log('4-box plan price:', price, '| per box:', perBox);

  // total mystery locks everything
  await page.click('#mystery-flower-box-surprise + label');
  const locked = await page.$eval('#mystery-flower-box-col-0', e => e.disabled);
  const summary2 = await page.$eval('#mystery-flower-box [data-builder-summary]', e => e.innerText);
  console.log('total mystery locks exclusions:', locked, '| summary:', summary2.trim());
  await page.click('#mystery-flower-box-surprise + label');  // back off

  // add to basket
  await page.click('[data-add]');
  await page.waitForTimeout(250);
  const count = await page.$eval('[data-basket-count]', e => e.textContent);
  console.log('basket count after add:', count);

  await page.goto(FILE + '#basket', { waitUntil: 'load' });
  await page.waitForTimeout(300);
  const basket = await page.evaluate(() => {
    const line = document.querySelector('.basket-line');
    return line ? line.innerText.replace(/\n+/g, ' | ') : 'EMPTY';
  });
  const total = await page.$eval('[data-basket-total]', e => e.textContent);
  console.log('basket line:', basket);
  console.log('basket total:', total);

  // --- gallery filter ------------------------------------------------------
  await page.goto(FILE + '#gallery', { waitUntil: 'load' });
  await page.waitForTimeout(200);
  const before = await page.$$eval('#gallery-grid .gallery-tile:not([hidden])', e => e.length);
  await page.click('#gallery [data-tab="golden-tickets"]');
  await page.waitForTimeout(150);
  const after = await page.$$eval('#gallery-grid .gallery-tile:not([hidden])', e => e.length);
  console.log('gallery tiles all/filtered:', before, '/', after);

  // --- locator search ------------------------------------------------------
  await page.goto(FILE + '#find-a-box', { waitUntil: 'load' });
  await page.waitForTimeout(200);
  await page.fill('[data-locator-search]', 'leeds');
  await page.waitForTimeout(150);
  const stock = await page.$$eval('[data-locator-item]:not([hidden])', e => e.map(x => x.querySelector('h4').textContent));
  console.log('locator search "leeds":', JSON.stringify(stock));

  // --- a form --------------------------------------------------------------
  await page.goto(FILE + '#contact', { waitUntil: 'load' });
  await page.waitForTimeout(200);
  await page.fill('#contact input[type=text]', 'John');
  await page.fill('#contact input[type=email]', 'john@example.com');
  await page.selectOption('#contact select', { index: 1 });
  await page.fill('#contact textarea', 'Testing the preview.');
  await page.check('#contact input[type=checkbox]');
  await page.click('#contact button[type=submit]');
  await page.waitForTimeout(250);
  const ok = await page.$eval('#contact [data-form-success]', e => !e.hidden && e.innerText.trim());
  console.log('contact form success:', JSON.stringify(ok));

  // --- screenshots ---------------------------------------------------------
  const shots = [
    ['home', 1280, 900], ['shop', 1280, 900], ['mystery-flower-box', 1280, 1400],
    ['gallery', 1280, 900], ['find-a-box', 1280, 900], ['corporate', 1280, 900],
  ];
  for (const [id, w, h] of shots) {
    await page.setViewportSize({ width: w, height: h });
    await page.goto(FILE + '#' + id, { waitUntil: 'load' });
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(700);
    await page.screenshot({ path: `${SHOTS}/${id}.png` });
  }
  await page.setViewportSize({ width: 390, height: 844 });
  for (const id of ['home', 'mystery-flower-box', 'gallery']) {
    await page.goto(FILE + '#' + id, { waitUntil: 'load' });
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(700);
    await page.screenshot({ path: `${SHOTS}/m-${id}.png` });
  }
  await page.goto(FILE + '#home', { waitUntil: 'load' });
  await page.waitForTimeout(400);
  await page.screenshot({ path: `${SHOTS}/full-home.png`, fullPage: true });

  console.log('console errors:', errors.length ? errors.slice(0, 8) : 'none');
  await browser.close();
})();
