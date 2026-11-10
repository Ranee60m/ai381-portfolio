# دليل تصوير 5–8 دقائق

هذا ترتيب للشرح والفهم؛ استخدم صوتك وكلماتك واسمك ورقمك الحقيقيين. أبقِ كل نتيجة على الشاشة 5 ثوانٍ على الأقل، وقل اسم كل Checkpoint. الفيديو MP4 بدقة 720p، الخط 14pt أو أكبر، والكاميرا ظاهرة.

- **0:00–0:30 — Checkpoint 0:** صفحة ملفك الشخصي في elearn.just.edu.jo تظهر الاسم والرقم لخمس ثوانٍ، ثم وجهك. قل اسمك ورقمك وLab 3 وتاريخ التسجيل الحقيقي. نفّذ `echo "AI381 YOUR_STUDENT_ID $(date)"` بعد استبدال الرقم.
- **0:30–1:45 — Checkpoint 1:** افتح MLflow على localhost:5000 وتجربة churn. أظهر المرشحين، params، data_sha256، metrics وملف MLmodel الذي يحتوي signature. اشرح أن hash يتغير إذا تغيّرت بايتات البيانات حتى لو بقي اسم الملف نفسه. split_seed=42 لتثبيت المقارنة، وليس ضماناً ضد تغيّر البيانات.
- **1:45–2:45 — Checkpoint 2:** قارن ثلاثة runs وافتح MODEL_SELECTION.md. اقرأ الأرقام الحقيقية واشرح لماذا اخترت البطل وما المقايضة في أسوأ شريحة والحجم والزمن. شرائح العقد لا تمثل وحدها تقييماً شاملاً للإنصاف.
- **2:45–3:45 — Checkpoint 3:** افتح PR الفرع lab3-worse-model وGitHub Actions بعد تنفيذ GITHUB_SETUP_AR.md. أظهر BLOCKED وخروج 1 والحماية من الدمج. اشرح شرط 30ms وفرق F1=0.01، وأن حظر المرشح لا يغيّر البطل. سجل التنفيذ المحلي موجود كدليل إضافي فقط.
- **3:45–4:45 — Checkpoint 4:** اعرض docker-compose.deploy.yml وrestart: unless-stopped، ثم `docker compose -f docker-compose.deploy.yml ps` و`bash scripts/smoke_test.sh http://localhost:8000`. اشرح أن restart يعيد العملية إذا تعطلت، وأن unhealthy وحده لا يعيدها تلقائياً في Compose.
- **4:45–5:45 — Checkpoint 5:** اعرض `/health` و`git rev-parse --short HEAD` و`docker images churn-api`. ابحث عن mlflow_run_id في MLflow، ثم أظهر git_sha وdata_sha256. commit الصورة هو إصدار البناء؛ tag الخاص بالـrun هو commit التدريب وقد يسبقه إذا أعدنا تعبئة بطل قديم.
- **5:45–6:45 — Checkpoint 6:** اشرح لماذا نثبت split ونحفظ المقاييس في Git لأن runner مؤقت. مقايضة: حد أدنى للتحسن يمنع تبديل البطل على مكسب ضئيل لكنه قد يرفض تحسناً صغيراً مفيداً. خطر: تكرار الاختيار على holdout نفسه يؤدي overfitting؛ نحتاج test مستقل وبيانات أحدث ومراقبة drift، ومراجعة الشرائح الصغيرة.

قبل التسليم تحقق أن الريبو يفتح وأن الـPR السيئ بقي دون دمج. الاسم:
`StudentID_FirstName_LastName_Lab3.mp4` بدون مسافات وبالاسم الرسمي.
ارفع الفيديو وrepo.txt إلى تكليف Lab 3 في Teams واضغط Turn in. الهوية والفيديو والتسليم الفعلي ينفذها الطالب.
