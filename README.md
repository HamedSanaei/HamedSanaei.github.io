# پرتفولیوی حامد ثنائی

سایت استاتیک سه‌زبانه با GitHub Pages، بدون سرور یا هاست جداگانه.

دامنهٔ تنظیم‌شده: `hamedsanaei.ir`؛ آدرس فارسی: `https://hamedsanaei.ir/fa/`.

| مسیر | زبان |
| --- | --- |
| `/fa/` | فارسی، زبان پیش‌فرض |
| `/en/` | انگلیسی |
| `/de/` | آلمانی |

ورودی `/` با انتقال فوری HTML به `/fa/` می‌رود. GitHub Pages مسیر `/fa` را هم به `/fa/` هدایت می‌کند.
محتوای هر زبان در HTML موجود است و به جاوااسکریپت نیاز ندارد. هر صفحه canonical مستقل، hreflang متقابل، x-default فارسی، متادیتای اشتراک‌گذاری و دادهٔ ساختاریافتهٔ Person دارد.

## ویرایش و پیش‌نمایش

ساختار و متن انگلیسی در `src/portfolio.html`، ترجمه‌ها در `src/translations.json`، مشخصات و لینک پروژه‌ها در `src/projects.json`، مشخصات سئو در `scripts/build_site.py` و ظاهر در `style.css` است. پس از ویرایش، خروجی‌ها را بسازید:

```powershell
python scripts/build_site.py
python scripts/check_site.py
python -m http.server 8765 --bind 127.0.0.1
```

پیش‌نمایش: <http://127.0.0.1:8765/>. بستهٔ پایتونی اضافه لازم نیست.
منابع و خروجی HTML باید با هم منتشر شوند. GitHub Pages از شاخهٔ `main` و پوشهٔ `/` منتشر می‌شود؛ `.nojekyll` حفظ شده است. build و check فقط محلی کار می‌کنند و commit، push یا انتشار انجام نمی‌دهند.

## اتصال hamedsanaei.ir از ایرنیک

دامنه به سرویس DNS نیاز دارد، ولی نیازی به خرید سرور نیست. یک گزینه، DNS رایگان Cloudflare است؛ میزبانی همچنان روی GitHub Pages می‌ماند.

۱. در [Cloudflare](https://dash.cloudflare.com/) دامنهٔ `hamedsanaei.ir` را اضافه و طرح **Free** را انتخاب کنید. دو Nameserver مخصوص همین دامنه را از پنل یادداشت کنید؛ مقدار آن‌ها نباید حدس زده شود.

۲. در [ایرنیک](https://www.nic.ir/) دامنه را انتخاب و در بخش کارگزارهای نام دامنه، همان دو Nameserver را وارد کنید. این قسمت محل ثبت IPهای GitHub نیست. منتظر فعال‌شدن دامنه در Cloudflare بمانید. اگر ثبت دامنه در انتظار تأیید است، ابتدا آن مرحله باید کامل شود.

۳. در [تنظیمات Pages حساب GitHub](https://github.com/settings/pages) دامنه را اضافه کنید. رکورد TXT نمایش‌داده‌شده را در Cloudflare ثبت و سپس Verify را بزنید. این رکورد مخصوص حساب شماست؛ پس از تأیید آن را نگه دارید.

۴. در [Settings → Pages مخزن](https://github.com/HamedSanaei/HamedSanaei.github.io/settings/pages)، **Custom domain** را `hamedsanaei.ir` قرار دهید. طبق راهنمای GitHub این کار باید پیش از تنظیم رکوردهای ترافیک وب انجام شود. مرحلهٔ بعد و انتشار فایل‌های دامنه را در همان نوبت انجام دهید تا فاصلهٔ انتقال کوتاه باشد.

۵. این رکوردها را در Cloudflare ثبت کنید؛ Proxy همه **DNS only** (ابر خاکستری) باشد و TTL می‌تواند Auto باشد:

| نوع | نام | مقدار |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | hamedsanaei.github.io |

رکوردهای پیش‌فرض متناقض مربوط به وب را اصلاح کنید؛ رکوردهای ایمیل و TXTهای تأیید را حفظ کنید. wildcard لازم نیست.

۶. پس از آماده‌بودن DNS، نسخهٔ مخصوص دامنه را محلی بسازید:

```powershell
python scripts/build_site.py --domain hamedsanaei.ir
python scripts/check_site.py
```

این فرمان `CNAME` را می‌سازد و canonicalها، hreflangها، آدرس تصاویر، دادهٔ ساختاریافته، sitemap و robots را به دامنهٔ جدید تغییر می‌دهد. buildهای بعدی دامنه را از CNAME می‌خوانند.
خروجی باید با مجوز انتشار commit و push شود. اگر تغییر دامنه در پنل GitHub یک commit ساخته باشد، آن را پیش از push ادغام کنید؛ force push لازم نیست.

۷. پس از موفقیت DNS check و صدور گواهی، **Enforce HTTPS** را در GitHub Pages فعال کنید. انتشار DNS ممکن است تا ۲۴ ساعت طول بکشد. GitHub آدرس github.io و www را به دامنهٔ اصلی هدایت می‌کند. آدرس فارسی نهایی `https://hamedsanaei.ir/fa/` است.

خروجی‌های فعلی برای `hamedsanaei.ir` ساخته شده‌اند و `CNAME` نیز همین دامنه را نگه می‌دارد. Nameserverهای اختصاص‌داده‌شده در این راه‌اندازی `adi.ns.cloudflare.com` و `dale.ns.cloudflare.com` هستند. دسترسی عمومی و HTTPS به تکمیل انتشار DNS و صدور گواهی GitHub بستگی دارد.

منابع: [تنظیم دامنه در GitHub](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)، [تنظیم Nameserver در Cloudflare](https://developers.cloudflare.com/dns/zone-setups/full-setup/setup/).

## ایندکس در گوگل

پس از انتشار، مالکیت سایت را در [Google Search Console](https://search.google.com/search-console/) تأیید کنید. برای دامنهٔ جدید، یک Domain Property با مقدار `hamedsanaei.ir` بسازید و TXT ارائه‌شدهٔ گوگل را در Cloudflare ثبت کنید.
برای آدرس فعلی GitHub، یک URL-prefix Property با مقدار `https://hamedsanaei.github.io/` بسازید و فایل HTML تأیید گوگل را بدون تغییر نام و محتوا در ریشهٔ پروژه منتشر کنید.

در Sitemaps، آدرس `sitemap.xml` میزبان فعال را ثبت کنید. سپس در URL Inspection برای `/fa/` درخواست ایندکس بدهید؛ `/en/` و `/de/` نیز در sitemap و لینک‌ها موجودند.
پس از انتقال دامنه، sitemap جدید `https://hamedsanaei.ir/sitemap.xml` را ثبت کنید. برای سایت قبلی و جدید، ابزار Change of Address را پس از بررسی پیش‌نیازهای آن به کار ببرید.

فارسی پیش‌فرض سایت است، اما زبان و آدرس نتیجهٔ گوگل به زبان کاربر، جست‌وجو و تصمیم گوگل هم بستگی دارد. ایندکس و زمان نمایش نتیجه تضمین‌شدنی نیست.

منابع: [نسخه‌های زبانی](https://developers.google.com/search/docs/specialty/international/localized-versions)، [انتقال فوری HTML](https://developers.google.com/search/docs/crawling-indexing/301-redirects)، [درخواست ایندکس](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl).
