import re
import random
import datetime
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)


# ==========================================
# 🧠 ADVANCED AI BRAIN (Expanded Knowledge Base)
# ==========================================

class StudyBrain:
    def __init__(self):
        self.intros = [
            "Here are a few strategies that usually help:",
            "Research suggests trying these approaches:",
            "Here are some proven methods for this:",
            "You might want to try these techniques:",
            "Let's tackle this with a few psychological tricks:",
            "Productivity experts often recommend these steps:",
            "Check out these actionable tips:"
        ]

        # Knowledge Topics (Keywords -> Responses)
        self.knowledge_base = {
            # --- SUBJECT SPECIFIC STRATEGIES ---
            # We give these keys a "boost" in scoring so they beat generic "tips"
            ("math", "calc", "algebra", "physics", "quantitative"): [
                "**Active Solving**: You cannot learn Math by reading. You must solve problems. If you get stuck, peek at the first step only, then try again.",
                "**The Mistake Log**: Keep a dedicated notebook for every problem you get wrong. Write down *why* you missed it. Review this before exams.",
                "**Derivations**: Don't just memorize formulas; understand how they are derived. It helps you solve 'twisted' questions.",
                "**Interleaving**: Mix up different types of problems (e.g., algebra then geometry) in one session. It stops your brain from auto-piloting."
            ],
            ("history", "lit", "english", "theory", "geography", "humanities"): [
                "**Storytelling**: Turn facts into a narrative. Our brains are wired to remember stories, not isolated dates.",
                "**Skeleton Arguments**: For essays, memorize key arguments and evidence points that can be adapted to almost any question prompt.",
                "**Mind Mapping**: Use visual webs to connect themes (e.g., 'Causes of WWII') rather than linear notes.",
                "**Quote Banks**: Memorize 10-15 versatile quotes that can apply to multiple themes or characters."
            ],
            ("cs", "computer", "code", "coding", "java", "python", "programming"): [
                "**Build to Learn**: You learn 10x faster by debugging a broken project than by following a tutorial perfectly.",
                "**Rubber Ducking**: Explain your code line-by-line to an inanimate object (or a duck). You'll often find the bug yourself while speaking.",
                "**Logic over Syntax**: Don't stress about memorizing exact syntax (you can Google that). Focus on understanding loops, recursion, and data structures.",
                "**Trace Tables**: Manually trace your loops on paper to truly understand how the variables change."
            ],
            ("bio", "biology", "chem", "chemistry", "science"): [
                "**Diagramming**: Draw processes (like the Krebs cycle) from memory. Visualizing the 'flow' is better than memorizing text.",
                "**Flashcards**: Use Anki for vocabulary-heavy topics. Science has a lot of specific terminology that needs rote memorization.",
                "**Real World Examples**: Connect chemical reactions or biological processes to things you see in daily life to anchor the memory.",
                "**Blurting**: Read a page, close the book, and write down everything you remember. Then check what you missed."
            ],

            # --- TIME MANAGEMENT ---
            ("time", "manage", "schedule", "routine", "late", "planning"): [
                "**The Eisenhower Matrix**: Categorize tasks into 4 boxes: Urgent/Important (Do First), Not Urgent/Important (Schedule), Urgent/Not Important (Delegate), Neither (Delete).",
                "**Eat the Frog**: Do your hardest, most dreaded task first thing in the morning. Your brain has the most willpower then.",
                "**Parkinson's Law**: Work expands to fill the time available. Set aggressive deadlines (e.g., 'I must finish this chapter in 40 mins') to force focus.",
                "**Time Blocking**: Don't just list tasks. Assign them specific hours (e.g., 'Math: 2pm-4pm'). A vague to-do list is the enemy of action.",
                "**The 2-Minute Rule**: If a task takes less than 2 minutes (like organizing files), do it immediately. Don't schedule it.",
                "**Review Day**: Spend Sunday evening planning your week. You wake up Monday morning knowing exactly what to execute.",
                "**Batching**: Group similar tasks together (e.g., reply to all emails at once) to avoid context-switching fatigue.",
                "**Pomodoro 2.0**: Try 50 minutes work, 10 minutes break. The standard 25/5 might be too short for deep work."
            ],
            # --- PROCRASTINATION & MOTIVATION ---
            ("procrastin", "start", "lazy", "motiv", "give up", "boring"): [
                "**The 5-Minute Rule**: Tell yourself you only have to study for 5 minutes. Usually, the pain is just in *starting*. Once you start, you'll likely keep going.",
                "**Motivation is a Myth**: Motivation follows action, it doesn't precede it. Start working, and the feeling of 'wanting to work' will follow.",
                "**Temptation Bundling**: Only allow yourself to listen to your favorite podcast or playlist *while* you are doing the boring work.",
                "**Visual Cues**: Put your books/laptop on your desk the night before. Remove the friction of setting up.",
                "**Forgive Yourself**: Research shows that forgiving yourself for procrastinating yesterday makes you less likely to procrastinate today.",
                "**Accountability Partner**: Tell a friend you'll send them $10 if you don't finish your chapter by 5 PM.",
                "**The 'Why'**: Write down why you are doing this. 'To get a good job' is vague. 'To buy a house by the ocean' is specific."
            ],
            # --- FOCUS & DISTRACTIONS ---
            ("distract", "phone", "focus", "concentrate", "attention", "social media"): [
                "**Phone Jail**: Put your phone in another room. Research shows that even seeing your phone screen (even if off) reduces cognitive capacity by 20%.",
                "**Binaural Beats**: Try listening to 40Hz binaural beats or 'Brown Noise'. It occupies the distracted part of your brain.",
                "**The Forest App**: Gamify your focus. If you pick up your phone, your digital tree dies. It sounds silly, but it works.",
                "**Single Tasking**: Multitasking is a lie. It's just rapid context-switching, which lowers your IQ by 10 points. Do one thing at a time.",
                "**Clear Desk, Clear Mind**: Physical clutter competes for your attention. Clear your workspace before starting.",
                "**Do Not Disturb**: Set your devices to DND mode automatically during study hours.",
                "**Browser Extensions**: Use 'StayFocusd' or 'Freedom' to block distracting websites during work hours."
            ],
            # --- MEMORY & LEARNING ---
            # Generic tips if no subject specified
            ("memory", "forget", "remember", "memoriz", "learn", "study", "tips", "tricks", "strategies", "strategy"): [
                "**Active Recall**: Don't just re-read notes (that's passive). Close the book and force your brain to retrieve the information. It should feel hard.",
                "**Spaced Repetition**: Review material at intervals: 1 day, 3 days, 1 week, 1 month. This fights the 'Forgetting Curve'.",
                "**The Feynman Technique**: Teach the concept to an empty chair (or a rubber duck). If you can't explain it simply, you don't understand it.",
                "**Sleep Sandwich**: Study hard, sleep, then review immediately upon waking. Sleep is when memory consolidation happens.",
                "**Dual Coding**: Combine words with images. Draw diagrams for everything. The brain has separate channels for visual and verbal info."
            ],
            # --- EXAM ANXIETY ---
            ("anxiety", "nervous", "panic", "scared", "stress", "worried"): [
                "**Physiological Sigh**: Inhale twice through your nose, then exhale long through your mouth. It mechanically resets your nervous system.",
                "**Reframe It**: Anxiety and Excitement are physiologically identical (high heart rate). Tell yourself 'I am excited', not 'I am scared'.",
                "**Brain Dump**: 10 minutes before the exam, write down all your worries. It offloads them from your working memory so you have more brain power for the test.",
                "**Perspective**: One exam does not define your worth or your future. Detach your ego from the result.",
                "**Visualization**: Visualize yourself calmly walking into the exam room and knowing the answers. It primes your brain for confidence."
            ],
            # --- NOTE TAKING ---
            ("note", "taking", "summar", "write"): [
                "**Cornell Method**: Divide page into cues (left), notes (right), and summary (bottom). It forces you to synthesize info, not just copy it.",
                "**Handwriting vs Typing**: Write by hand. It forces you to process the meaning because you can't write as fast as the lecturer speaks.",
                "**Mind Mapping**: Use non-linear notes to connect ideas. Great for history or literature themes.",
                "**Question-Based Notes**: Instead of writing headers like 'Photosynthesis', write 'How does Photosynthesis work?'. It primes your brain for answers."
            ]
        }

        self.fallbacks = [
            "That's a complex topic. Breaking it down into small, manageable steps is usually the best start.",
            "Consistency beats intensity. 30 minutes every day is better than 5 hours on Sunday.",
            "Try to study in the same place every day. Context-dependent memory helps recall.",
            "Could you tell me more about what you're studying? I can give better advice.",
            "Remember to hydrate. A 2% drop in hydration can lead to a 20% drop in focus."
        ]

    def get_response(self, text):
        text = text.lower()
        best_match = None
        highest_score = 0

        # Scoring System
        for keywords, responses in self.knowledge_base.items():
            score = 0
            for k in keywords:
                if k in text:
                    score += 1

            # TIE BREAKER Logic:
            # If the user asks for "Strategies for Math", both "Strategies" (General) and "Math" (Subject) match.
            # We want "Math" to win.
            # Simple heuristic: If the key contains subject names (math, history, etc), give it a bonus point.
            is_subject_key = any(x in keywords for x in ['math', 'history', 'cs', 'bio', 'physics', 'chem', 'lit'])
            if is_subject_key and score > 0:
                score += 1

            if score > highest_score:
                highest_score = score
                best_match = responses

        if highest_score > 0:
            # Pick 3 random tips, shuffled for variety
            shuffled_tips = random.sample(best_match, min(3, len(best_match)))

            intro = random.choice(self.intros)

            # Format as HTML list
            body = "<ul class='list-disc pl-5 space-y-2 mt-2'>"
            for tip in shuffled_tips:
                body += f"<li>{tip}</li>"
            body += "</ul>"

            return f"{intro} {body}"

        return random.choice(self.fallbacks)


brain = StudyBrain()


# ==========================================
# 🛠️ FLEXIBLE PARSING ENGINE
# ==========================================

def format_duration(minutes_input):
    rounded = int(5 * round(float(minutes_input) / 5))
    if rounded < 5: rounded = 5

    hours = rounded // 60
    minutes = rounded % 60

    parts = []
    if hours > 0: parts.append(f"{hours}hrs")
    if minutes > 0: parts.append(f"{minutes}mins")
    return " ".join(parts) if parts else "5mins"


# Global aliases map for use in both extraction and intent detection
ALIASES = {
    'maths': 'Mathematics', 'math': 'Mathematics', 'calc': 'Calculus',
    'phy': 'Physics', 'chem': 'Chemistry', 'bio': 'Biology',
    'cs': 'Computer Science', 'comp sci': 'Computer Science', 'coding': 'Coding',
    'eng': 'English', 'eco': 'Economics', 'biz': 'Business',
    'psych': 'Psychology', 'socio': 'Sociology', 'stats': 'Statistics',
    'pol sc': 'Political Science', 'political science': 'Political Science'
}


def extract_subjects_robust(text):
    text_lower = text.lower()

    # 1. STRATEGY: Isolate the "List" part of the sentence
    content = text_lower
    intro_patterns = [
        r'plan for', r'schedule for', r'study', r'studying', r'subjects are',
        r'subject is', r'cover', r'covering', r'help with', r'track', r'my subjects:'
    ]

    for p in intro_patterns:
        parts = re.split(p, content, maxsplit=1)
        if len(parts) > 1:
            content = parts[1]
            break

    # 2. FLATTEN EVERYTHING TO WORDS (Aggressive Splitting)
    # Split by: comma, space, "and", &, +, /, |, or newline
    # This forces "Math Physics" to become ['Math', 'Physics']
    raw_tokens = re.split(r'[\s,;&+/|]+|\band\b', content)

    ignore_words = {
        'make', 'a', 'plan', 'for', 'the', 'please', 'help', 'me', 'i', 'want', 'to', 'need',
        'hours', 'hour', 'days', 'day', 'week', 'schedule', 'timetable', 'advice', 'tips',
        'weak', 'strong', 'weakest', 'strongest', 'subjects', 'subject', 'daily', 'every', 'is', 'are',
        'hi', 'hello', 'hey', 'greetings', 'sup'
    }

    # Clean Tokens
    tokens = []
    for t in raw_tokens:
        clean = t.strip()
        # Keep distinct words that are not ignored
        if clean and clean not in ignore_words and not clean.isdigit():
            tokens.append(clean)

    # 3. RECONSTRUCT MULTI-WORD SUBJECTS (Only known ones)
    final_subjects = []

    # Known multi-word subjects to stitch back together
    known_multi = {
        'computer science', 'political science', 'social studies', 'web dev', 'web development',
        'business studies', 'information technology', 'artificial intelligence', 'machine learning',
        'data structures', 'operating systems', 'linear algebra', 'discrete math', 'applied math',
        'organic chemistry', 'physical chemistry', 'ancient history', 'modern history', 'english literature',
        'software engineering', 'environmental science'
    }

    i = 0
    while i < len(tokens):
        current_word = tokens[i]

        # Look ahead for combination
        if i + 1 < len(tokens):
            next_word = tokens[i + 1]
            combined = f"{current_word} {next_word}"

            # Check against known multi-word list
            if combined in known_multi:
                final_subjects.append(combined.title())
                i += 2
                continue

        # Default: Add single word (e.g., "Maths", "Physics", "CS")
        final_subjects.append(current_word.title())
        i += 1

    # Remove duplicates preserving order
    return list(dict.fromkeys(final_subjects))


def parse_request(text):
    text_lower = text.lower()

    # Days detection
    days = 5
    d_match = re.search(r'(\d+)\s*days?', text_lower)
    if d_match: days = int(d_match.group(1))

    # Hours detection
    hours = 4.0
    h_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:hours?|hrs?|h)', text_lower)
    if h_match: hours = float(h_match.group(1))

    # Subject Extraction
    subjects = extract_subjects_robust(text)

    # Weak/Best Detection
    weakest, best = None, None

    for s in subjects:
        # Check against the exact name user typed
        pat = re.escape(s.lower())

        # Weakest Logic
        if re.search(rf'weakest\s*(?:subject)?\s*(?:is)?\s*{pat}\b', text_lower):
            weakest = s
        elif re.search(rf'(bad|suck|hate|struggle|fail|hard|worst).*?{pat}\b', text_lower):
            if not weakest: weakest = s

            # Best Logic
        if re.search(rf'strongest\s*(?:subject)?\s*(?:is)?\s*{pat}\b', text_lower):
            best = s
        elif re.search(rf'(good|love|easy|ace|best|strong).*?{pat}\b', text_lower):
            if s != weakest: best = s

    return {
        'days': days,
        'daily_hours': hours,
        'subjects': subjects,
        'weakest': weakest,
        'best': best
    }


# ==========================================
# 📅 SCHEDULING ENGINE
# ==========================================

def generate_schedule(constraints):
    days = constraints['days']
    daily_hours = constraints['daily_hours']
    subjects = constraints['subjects']
    weakest = constraints['weakest']
    best = constraints['best']

    if not subjects:
        return None

    schedule = []
    task_types = ["Concept Review", "Practice Problems", "Active Recall", "Mock Questions"]

    # Time Calculation
    total_minutes = daily_hours * 60
    num_sub = len(subjects)

    # Weights: Weakest (1.5 - MORE time), Normal (1.0), Strongest (0.5 - LESS time)
    # Total shares calculation
    shares = 0
    for s in subjects:
        if s == weakest:
            shares += 1.5  # Increased time for weakest
        elif s == best:
            shares += 0.5  # Reduced time for best
        else:
            shares += 1.0  # Standard time for normal

    if shares == 0: shares = num_sub  # Fallback
    base_unit = total_minutes / shares

    for d in range(1, days + 1):
        day_plan = []

        for i, sub in enumerate(subjects):
            is_weakest = (sub == weakest)
            is_best = (sub == best)

            # Time Allocation
            if is_weakest:
                dur = base_unit * 1.5
            elif is_best:
                dur = base_unit * 0.5
            else:
                dur = base_unit * 1.0

            dur_str = format_duration(dur)

            # Task Rotation
            task_idx = (d + i) % len(task_types)
            task = task_types[task_idx]

            # Formatting
            if is_weakest:
                row = f"<span class='text-red-600 font-bold'>⚠️ {sub} (Deep Dive)</span>: {task} ({dur_str})"
            elif is_best:
                row = f"<span class='text-green-600 font-bold'>✨ {sub} (Quick)</span>: Speed Review ({dur_str})"
            else:
                row = f"<b>{sub}</b>: {task} ({dur_str})"

            day_plan.append(row)

        schedule.append({'day': f"Day {d}", 'sessions': day_plan})

    return {
        'schedule': schedule,
        'meta': {
            'weakest': weakest,
            'best': best,
            'count': num_sub
        }
    }


# ==========================================
# 🌐 FLASK ROUTES
# ==========================================

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    text = data.get('text', '')
    text_lower = text.lower()

    # 1. Parse
    constraints = parse_request(text)

    # 2. Determine Intent
    has_subjects = len(constraints['subjects']) > 0

    # Intent Flags
    is_greeting = re.search(r'\b(hi|hello|hey|greetings|grettings|sup|yo|good\s*(morning|evening|afternoon))\b',
                            text_lower)
    is_gratitude = 'thank' in text_lower

    # Expanded advice triggers - ADDED "STRATEGY"
    advice_keywords = ['tip', 'advice', 'how to', 'help me', 'help with', 'struggle', 'distract', 'focus', 'tired',
                       'manage time', 'time management', 'strategy', 'strategies', 'trick', 'method']
    is_advice = any(x in text_lower for x in advice_keywords)

    # Explicit Plan Request Check
    plan_keywords = ['plan', 'schedule', 'timetable', 'routine', 'make', 'create', 'organize', 'build']
    is_plan_request = any(x in text_lower for x in plan_keywords)

    # 3. Execution Priority

    # Priority A: Explicit Advice Request (Overrides Planning)
    if is_advice:
        ai_response = brain.get_response(text)
        return jsonify({"type": "text", "message": ai_response})

    # Priority B: Greetings (only if no subjects)
    if is_greeting and len(text) < 50 and not has_subjects:
        responses = [
            "Hi there! I'm your Academic Advisor. Do you need a study plan or some study tips?",
            "Hello! Ready to get organized? Tell me your subjects or ask for advice.",
            "Hey! I can help you build a timetable or solve study problems. What do you need?"
        ]
        return jsonify({"type": "text", "message": random.choice(responses)})

    # Priority C: Make a Plan (ONLY if subjects detected AND explicit plan keyword used)
    if has_subjects and is_plan_request:
        plan = generate_schedule(constraints)
        if plan:
            msg = f"Created a custom plan for <b>{len(constraints['subjects'])} subjects</b>."
            if plan['meta']['weakest']:
                msg += f"<br> ⬆️ Deep Dive for <b>{plan['meta']['weakest']}</b> (Weakest)."
            if plan['meta']['best']:
                msg += f"<br> ⬇️ Quick Review for <b>{plan['meta']['best']}</b> (Strongest)."
            return jsonify({"type": "plan", "message": msg, "data": plan})

    # Priority D: Subjects detected but NO plan request
    if has_subjects and not is_plan_request:
        subject_list = ", ".join(constraints['subjects'])
        return jsonify({
            "type": "text",
            "message": f"I see you're studying <b>{subject_list}</b>. Would you like me to create a <b>timetable</b> for these, or do you need <b>study tips</b>?"
        })

    if is_gratitude:
        return jsonify({"type": "text", "message": "You're welcome! Consistency is key. You got this!"})

    # Priority E: AI Brain (General Fallback)
    if len(text) > 2:
        ai_response = brain.get_response(text)
        return jsonify({"type": "text", "message": ai_response})

    return jsonify({"type": "text",
                    "message": "I didn't detect a clear request. Try saying: 'Make a plan for Math and Physics' or 'Tips for focus'."})


# ==========================================
# 🖥️ FRONTEND
# ==========================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Academic Advisor</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background: #f0f2f5; font-family: 'Inter', sans-serif; }
        .chat-scroll { height: calc(100vh - 140px); overflow-y: auto; }
        .msg-user { background: #2563eb; color: white; border-radius: 18px 18px 0 18px; }
        .msg-bot { background: white; color: #1f2937; border-radius: 18px 18px 18px 0; border: 1px solid #e5e7eb; }
        .typing span { animation: blink 1.4s infinite; display: inline-block; width: 4px; height: 4px; background: #9ca3af; border-radius: 50%; margin: 0 1px; }
        .typing span:nth-child(2) { animation-delay: 0.2s; }
        .typing span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes blink { 0%, 100% { opacity: 0.2; transform: scale(0.8); } 50% { opacity: 1; transform: scale(1.2); } }
    </style>
</head>
<body class="flex flex-col h-screen">

    <!-- Header -->
    <div class="bg-white shadow px-6 py-4 flex justify-between items-center z-10">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600">
                <i class="fa-solid fa-brain"></i>
            </div>
            <div>
                <h1 class="font-bold text-gray-800">Academic Advisor AI</h1>
                <div class="flex items-center gap-1">
                    <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                    <span class="text-xs text-gray-500">Online & Ready</span>
                </div>
            </div>
        </div>
        <button onclick="location.reload()" class="text-gray-400 hover:text-blue-600"><i class="fa-solid fa-rotate"></i></button>
    </div>

    <!-- Chat Area -->
    <div id="chat-box" class="chat-scroll p-4 space-y-4 max-w-3xl mx-auto w-full">
        <!-- Intro -->
        <div class="flex gap-3">
            <div class="w-8 h-8 bg-blue-100 rounded-full flex-shrink-0 flex items-center justify-center text-blue-600"><i class="fa-solid fa-robot"></i></div>
            <div class="msg-bot p-4 shadow-sm max-w-[85%]">
                <p>Hello! I'm your advanced study assistant. I can:</p>
                <ul class="list-disc ml-5 mt-2 text-sm text-gray-600">
                    <li><b>Generate Plans:</b> "Plan for Math, Physics, and Bio for 3 days."</li>
                    <li><b>Solve Problems:</b> "I'm always distracted by my phone."</li>
                    <li><b>Give Tips:</b> "How do I take better notes?"</li>
                </ul>
            </div>
        </div>
    </div>

    <!-- Input -->
    <div class="bg-white border-t p-4">
        <div class="max-w-3xl mx-auto relative">
            <input type="text" id="user-input" 
                class="w-full bg-gray-100 rounded-full pl-5 pr-12 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Ask anything study related..." autocomplete="off">
            <button onclick="send()" class="absolute right-2 top-2 w-8 h-8 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition">
                <i class="fa-solid fa-arrow-up"></i>
            </button>
        </div>
    </div>

    <script>
        const chat = document.getElementById('chat-box');
        const inp = document.getElementById('user-input');

        inp.addEventListener('keypress', (e) => { if(e.key === 'Enter') send(); });

        function addMsg(text, isUser, isHtml=false) {
            const div = document.createElement('div');
            div.className = `flex gap-3 ${isUser ? 'justify-end' : ''}`;

            const avatar = isUser ? '' : `<div class="w-8 h-8 bg-blue-100 rounded-full flex-shrink-0 flex items-center justify-center text-blue-600"><i class="fa-solid fa-robot"></i></div>`;

            const content = `
                <div class="${isUser ? 'msg-user' : 'msg-bot'} p-3 px-4 shadow-sm max-w-[85%]">
                    ${isHtml ? text : `<p>${text}</p>`}
                </div>`;

            div.innerHTML = isUser ? content : avatar + content;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }

        async function send() {
            const txt = inp.value.trim();
            if(!txt) return;

            inp.value = '';
            addMsg(txt, true);

            // Loading
            const loadId = 'load-'+Date.now();
            const loader = document.createElement('div');
            loader.id = loadId;
            loader.className = "flex gap-3";
            loader.innerHTML = `<div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-600"><i class="fa-solid fa-robot"></i></div><div class="msg-bot p-3 typing"><span></span><span></span><span></span></div>`;
            chat.appendChild(loader);
            chat.scrollTop = chat.scrollHeight;

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: txt})
                });
                const data = await res.json();
                document.getElementById(loadId).remove();

                if(data.type === 'plan') renderPlan(data.message, data.data);
                else addMsg(data.message, false);

            } catch(e) {
                document.getElementById(loadId).remove();
                addMsg("My brain is offline briefly. Try again.", false);
            }
        }

        function renderPlan(msg, data) {
            addMsg(msg, false, true);

            let html = `<div class="space-y-3 mt-2 w-full">`;
            data.schedule.forEach(day => {
                html += `
                    <div class="bg-gray-50 rounded-lg border border-gray-200 p-3">
                        <div class="font-bold text-blue-800 text-sm mb-2 border-b border-gray-200 pb-1">${day.day}</div>
                        <ul class="text-sm space-y-2">
                            ${day.sessions.map(s => `<li class="flex items-start gap-2"><i class="fa-solid fa-check-circle text-gray-300 mt-1"></i> <span>${s}</span></li>`).join('')}
                        </ul>
                    </div>
                `;
            });
            html += `</div>`;

            addMsg(html, false, true);
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)