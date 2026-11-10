# إكمال GitHub والفيديو

لم يُنشأ مستودع بعيد ولم تُنفّذ GitHub Actions في هذه البيئة: رمز GitHub المتاح غير صالح. لا تشارك كلمات المرور أو الرموز في المحادثة؛ نفّذ `gh auth login` محلياً أو استخدم واجهة GitHub.

## رفع المشروع

تأكد أولاً من فهم الملفات ونتائجها، واستخدم هويتك أنت في إعدادات Git. أرشيف المشروع يتضمن تاريخ Git محلياً حتى تعمل أوامر تتبع SHA والفرع الضعيف.

```bash
git switch lab3
git config user.name "YOUR_NAME"
git config user.email "YOUR_EMAIL"
gh auth login
# اختر اسم مستودعك الحقيقي؛ أنشئه فارغاً من GitHub ثم:
git remote add origin https://github.com/OWNER/REPO.git
git push -u origin lab3
```

لإظهار أول PR أخضر دون مقارنة البطل بنفسه، أنشئ main من أول commit الذي يسبق ملفات البطل:

```bash
git branch main $(git rev-list --max-parents=0 lab3)
git push -u origin main
# في GitHub Settings > General اجعل main الفرع الافتراضي
# ثم افتح PR:
gh pr create --base main --head lab3 --title "Lab 3: tracked champion and local deployment" --body "MLflow candidates, measured selection, promotion gate and local Docker smoke test."
```

أول commit لا يحتوي champion.json، فيكون أول gate مؤهلاً للترقية. بعد نجاح `test` و`train and gate` ادمج PR من GitHub. قد يُحظر تشغيل main اللاحق إذا كانت النتيجة مساوية للبطل المحفوظ؛ هذا سلوك مقصود لقاعدة الحد الأدنى للتحسّن. النشر المحلي يعمل بالبطل المحفوظ ولا يحتاج ترقية جديدة.

في Settings > Rules > Rulesets أو Branches أضف حماية main، وRequire status checks، واختر `test` و`train and gate` بعد ظهورهما. حظر الدمج يتطلب تفعيل الحماية؛ اللون الأحمر وحده لا يمنع كل أصحاب الصلاحيات من الدمج.

## الـPR الضعيف المطلوب

الفرع `worse-model` المرفق يغيّر CANDIDATES إلى logistic ضعيف فقط. بعد دمج lab3:

```bash
git push -u origin worse-model
gh pr create --base main --head worse-model --title "Demonstrate blocked weak model" --body "Intentionally weak C=0.00001 candidate; expected BLOCKED gate. Do not merge."
```

افتح Actions، اعرض خطوة Promotion gate ورسالة BLOCKED، وسجّلها في الفيديو مع زر الدمج المحظور. لا تدمج هذا الفرع. إذا لم تظهر نتائج الفروع، تأكد أن main والـPR موجودان وأن Actions مفعّل في المستودع.

بعد إنشاء المستودع الحقيقي، أنشئ ملف التسليم:

```bash
printf '%s\n' 'https://github.com/OWNER/REPO' > repo.txt
```

استبدل OWNER/REPO فعلياً. لا تسلّم رابطاً وهمياً.
