# رفع Lab 3 إلى مستودعك الحالي

المستودع: https://github.com/Ranee60m/ai381-portfolio

تم تجهيز Lab 3 داخل `lab3/` مع إبقاء Lab 2 وworkflow الخاص به. الفرع `lab3-complete` مبني على main الحقيقي للمستودع ويضم تاريخ مصدر التدريب الأصلي للمحافظة على تتبع SHA. الفرع `lab3-worse-model` يضيف المرشح الضعيف فقط.

## الدخول والرفع

لا تضع كلمات مرور أو tokens في المحادثة أو الملفات. إذا لم يكن GitHub متصلاً ببيئة العمل، سجّل الدخول على جهازك:

```bash
gh auth login
git config user.name "YOUR_NAME"
git config user.email "YOUR_EMAIL"
git switch lab3-complete
git push -u origin lab3-complete
gh pr create --repo Ranee60m/ai381-portfolio --base main --head lab3-complete --title "Lab 3: tracked champion and local Docker deployment" --body "Adds lab3 without changing lab2: MLflow tracking, measured model selection, promotion gate, and local Docker smoke test."
```

أول PR يقارن مع `lab3/artifacts/champion.json` من main. لا يوجد هذا الملف في main الحالي، لذلك يمكن ترقية أول مرشح مؤهل. انتظر نجاح `Lab 3 test` و`train and gate` وكذلك فحص Lab 2 الموجود. راجع ثم ادمج الـPR من GitHub.

في Settings > Rules > Rulesets أو Branches أضف `Lab 3 test` و`train and gate` إلى الفحوص المطلوبة على main مع إبقاء الحماية الحالية. يظهر اسم الفحص بعد تشغيله. حظر الدمج يحتاج حماية الفرع؛ اللون الأحمر وحده لا يمنع جميع أصحاب الصلاحيات من الدمج.

## إظهار النموذج الضعيف

بعد دمج الفرع الجيد:

```bash
git push -u origin lab3-worse-model
gh pr create --repo Ranee60m/ai381-portfolio --base main --head lab3-worse-model --title "Demonstrate blocked weak model" --body "Intentionally weak C=0.00001 candidate; expected BLOCKED promotion gate. Do not merge."
```

اعرض Actions > Lab 3 train-and-gate > Promotion gate ورسالة BLOCKED، وزر الدمج المحظور في الفيديو. لا تدمج هذا الفرع.

بوابة الترقية ترفض حتى النموذج المساوي للبطل. لذلك قد تُحظر إعادة تدريب نفس المرشحين على main في تشغيل لاحق؛ هذا متوقع. النشر المحلي يستخدم البطل المحفوظ ولا يحتاج ترقية جديدة.

## التشغيل والتسليم

من جذر المستودع:

```bash
cd lab3
bash scripts/run_local.sh
```

ملف `repo.txt` في جذر المستودع يحتوي الرابط الحقيقي. الفيديو ورفع Teams ينفذهما الطالب بهويته وصوته ووجهه وفق `VIDEO_GUIDE_AR.md`.
