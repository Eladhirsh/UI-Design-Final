from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "replace_with_a_secure_random_key"

# ── Boroughs data ─────────────────────────────────────────────────────────────

boroughs_data = {
    "Manhattan": [
        {
            "name": "Bagels with Lox and Cream Cheese",
            "image": "https://dempsters.ca/sites/default/files/styles/recipes_full_467x341_/public/2021-02/Lox%20Cream%20Cheese%20Bagel-061_1800x750-min.jpg?itok=o1vyYifd",
            "description": "Brought by Eastern European Jewish immigrants, this bagel combo became a New York classic through Jewish delis and appetizing shops."
        },
        {
            "name": "New York-Style Pizza",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfumj-0zAhLdubseE8dlivjnBJpj5d9WA0VQ&s",
            "description": "Inspired by Italian immigrants and adapted to New Yorkers' fast-paced lifestyle with large, foldable slices."
        },
        {
            "name": "Pastrami on Rye",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSa029FDOXouTpPm0XFwq_pFjBygu8rbdgMZw&s",
            "description": "A product of Jewish delicatessen culture, with Romanian roots in the art of curing and spicing meats."
        },
        {
            "name": "Cheesecake",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTqfjBgGCw-BalSew1oSFvI8xArN4w5_vpbdQ&s",
            "description": "Originating from Eastern European Jewish bakers, New York cheesecake is known for its rich cream cheese base and smooth texture."
        },
        {
            "name": "Halal Chicken Over Rice",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSIRhMPVFmJW-fuYK1jKwrxYF4SDWhNcNInSw&s",
            "description": "Popularized by Egyptian and Middle Eastern street vendors, this dish reflects the growth of Muslim immigrant communities in the city."
        }
    ],
    "Brooklyn": [
        {
            "name": "Artisan Pizza",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbIVYrS6TrLGaxZHs0ekSBj4nqYVZbu8rknQ&s",
            "description": "Reflects the Italian-American tradition of hand-tossed pizza, elevated by Brooklyn’s focus on craftsmanship and fresh ingredients."
        },
        {
            "name": "Smoked Meats & BBQ",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTBm9qOf-PEyL3EZ5n0rfg2YyjDt1b6ajTsjw&s",
            "description": "A nod to Southern American barbecue culture, embraced by Brooklyn’s growing community of pitmasters and food artisans."
        },
        {
            "name": "Pierogi & Eastern European Food",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLW8xFQdnouDmUag0QpVBc5ubHj4BM9SU4cw&s",
            "description": "Introduced by Polish immigrants, pierogi remain a staple in Brooklyn's historically Polish neighborhoods."
        },
        {
            "name": "Rainbow Bagels",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRD3DT_pSKEzTxcpkc2TIHFEFvEaX2tBu0umg&s",
            "description": "A playful modern twist on traditional Jewish bagels, invented in Brooklyn to combine creativity with culinary tradition."
        },
        {
            "name": "Caribbean Jerk Chicken",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZPkHa1Ls1BG6x5ImJZnKSgQ20bz_PKGMauQ&s",
            "description": "Brought by Jamaican and West Indian immigrants, this spicy dish is a flavorful symbol of Brooklyn’s Caribbean heritage."
        }
    ],
    "Bronx": [
        {
            "name": "Chopped Cheese Sandwich",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwS9daa2Cy2BrnvkY7-r7B74YpCX0z9uD2tA&s",
            "description": "A Bronx-born sandwich, created by local bodegas as a quick, affordable twist on the cheeseburger."
        },
        {
            "name": "Mofongo",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4cGqTRv8kkbnP7wRehOGcfMhWVwosqh_vlg&s",
            "description": "Rooted in Puerto Rican and Afro-Caribbean culinary traditions, using mashed plantains as a flavorful base."
        },
        {
            "name": "Empanadas",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSkc9ExwaRzudHXnFvARmN3fzg2TmFrcfPZig&s",
            "description": "Originally from Spain and adapted across Latin America, empanadas are a handheld favorite filled with seasoned meats or veggies."
        },
        {
            "name": "Italian Deli Sandwich",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQN5AoK5dD6ODJqcHG1u3Q4kAkDzhnYPN5y8A&s",
            "description": "Reflect the strong Italian-American presence in the Bronx, with influences from classic Italian charcuterie."
        },
        {
            "name": "Mangú",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTrJ6N_d_jU3nPfe54Zk_hFO73c4aviormSZA&s",
            "description": "A Dominican staple with African roots, traditionally served with eggs, cheese, and salami."
        }
    ],
    "Queens": [
        {
            "name": "Chinese Dumplings",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTePskvZH1Rxt3j6DriUyoJAb0q5HHbJsfuYA&s",
            "description": "Brought by Chinese immigrants, these dumplings are central to Cantonese and Northern Chinese culinary traditions."
        },
        {
            "name": "Arepas",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmjAPs6VNn2oR5r6QVOgIWSQVwsoN5Pfv6Bg&s",
            "description": "A staple of Colombian and Venezuelan street food, made from cornmeal and filled with cheese, meats, or beans."
        },
        {
            "name": "Thai Food",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ7bBWBOhR65bVfigJW0PqVHM8PXmqM3n8atw&s",
            "description": "Thai immigrants introduced their balanced, flavorful dishes of sweet, sour, salty, and spicy to Queens' dining scene."
        },
        {
            "name": "Indian Curry & Dosas",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpJivCCXW_14iTjVaacn0ZXVVKG7EMv1Oteg&s",
            "description": "Reflecting South Asian immigration, these dishes highlight the complex spices and flavors of Indian cuisine."
        },
        {
            "name": "Greek Souvlaki",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRH-bBCJ9Utd5yIHzUqCqRY5v1XzTAmysbqRjDDMZfeOReyQ85P",
            "description": "Brought by Astoria’s historic Greek community, these grilled meat dishes are a cornerstone of Greek street food."
        }
    ],
    "Staten Island": [
        {
            "name": "Italian-Style Pizza",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-zzaX0hmC8Ry56fkoAarkG5SQrDDwLNxCeQ&s",
            "description": "Reflects Staten Island’s deep Italian-American roots, with many pizzerias perfecting Sicilian-style thick crusts."
        },
        {
            "name": "Mozzarella & Prosciutto Sandwiches",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_whr_nj2d3EOvIJ8ZmbkoeBsV-mxG6Ent4g&s",
            "description": "Inspired by traditional Italian antipasto, these sandwiches showcase Italian mastery of cured meats and fresh cheeses."
        },
        {
            "name": "Seafood Pasta",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQaIbdGb2gFrS_g8A5uUnYQtQUGng9DWqBB6g&s",
            "description": "Draws from Southern Italian coastal recipes, emphasizing fresh seafood and simple preparations."
        },
        {
            "name": "Sausage & Peppers Hero",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTs3WTTA8sbLUIVHKYNxFH2Sf__l3kD-gazAA&s",
            "description": "An Italian-American street fair staple, celebrating the flavors of sweet and spicy sausage with sautéed bell peppers."
        },
        {
            "name": "Cannoli",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSy-usG9ZnBM7E8JrGzmMJOUbIxQ4wMFuGQWQ&s",
            "description": "Sicilian in origin, cannoli were brought by Italian immigrants and became a beloved dessert across New York."
        }
    ]
}

# ── Quiz questions (single definition) ──────────────────────────────────────────

quiz_questions = [
    # multiple‐choice
    {"id":"q1","type":"mc","text":"Which borough is famous for chopped cheese sandwiches?","options":["Manhattan","Brooklyn","The Bronx","Queens"],"correct":"The Bronx"},
    {"id":"q2","type":"mc","text":"Which borough is known for Greek souvlaki?","options":["Staten Island","Queens","The Bronx","Manhattan"],"correct":"Queens"},
    {"id":"q3","type":"mc","text":"Which borough has the iconic \"Bagels with Lox and Cream Cheese\"?","options":["Manhattan","Brooklyn","Staten Island","Queens"],"correct":"Manhattan"},
    {"id":"q4","type":"mc","text":"Where would you most likely find Rainbow Bagels?","options":["Manhattan","Brooklyn","The Bronx","Queens"],"correct":"Brooklyn"},
    # true/false
    {"id":"q5","type":"tf","text":"Mangú is a traditional dish from Queens.","correct":"False"},
    {"id":"q6","type":"tf","text":"Cheesecake originated from Manhattan.","correct":"True"},
    {"id":"q7","type":"tf","text":"Artisan Pizza comes from Staten Island.","correct":"False"},
    # drag & drop
    {"id":"q8","type":"drag_and_drop","text":"Drag the correct Bronx food onto the borough map.","image":"https://images.squarespace-cdn.com/content/v1/57154d604d088e8318875db8/a013d86b-ddcf-4f4c-9fe3-2c94e7944369/Bronx+Neighborhoods+Titles.png?format=1000w","options":[
        {"name":"Chopped Cheese","image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgEJvFpfDgNpDc126etU3bD6R2fk_1IFSwxw&s","is_correct":True},
        {"name":"Rainbow Bagel","image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRD3DT_pSKEzTxcpkc2TIHFEFvEaX2tBu0umg&s","is_correct":False},
        {"name":"Arepas","image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmjAPs6VNn2oR5r6QVOgIWSQVwsoN5Pfv6Bg&s","is_correct":False},
        {"name":"Pierogi","image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLW8xFQdnouDmUag0QpVBc5ubHj4BM9SU4cw&s","is_correct":False}
    ]},
    {"id":"q9","type":"drag_and_drop","text":"Drag the correct Queens dish onto the map.","image":"https://images.squarespace-cdn.com/content/v1/57154d604d088e8318875db8/1b3e757e-0ce1-4822-bfa4-aca169b5f550/Queens-Neighborhoods-Map.png?format=1000w","options":[
        {"name":"Chinese Dumplings","image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTePskvZH1Rxt3j6DriUyoJAb0q5HHbJsfuYA&s","is_correct":True},
        {"name":"Cheesecake","image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTqfjBgGCw-BalSew1oSFvI8xArN4w5_vpbdQ&s","is_correct":False},
        {"name":"Pastrami on Rye","image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSa029FDOXouTpPm0XFwq_pFjBygu8rbdgMZw&s","is_correct":False},
        {"name":"Jerk Chicken","image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZPkHa1Ls1BG6x5ImJZnKSgQ20bz_PKGMauQ&s","is_correct":False}
    ]},
    {"id":"q10","type":"drag_and_drop","text":"Drag the Staten Island specialty onto its map.","image":"https://images.squarespace-cdn.com/content/v1/57154d604d088e8318875db8/349a469c-68d4-4c5a-8035-0433f980ecc3/Staten+Island+Neighborhood+Map.png?format=1000w","options":[
        {"name":"Italian-Style Pizza","image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-zzaX0hmC8Ry56fkoAarkG5SQrDDwLNxCeQ&s","is_correct":True},
        {"name":"Halal Chicken Over Rice","image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSIRhMPVFmJW-fuYK1jKwrxYF4SDWhNcNInSw&s","is_correct":False},
        {"name":"Mofongo","image":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4cGqTRv8kkbnP7wRehOGcfMhWVwosqh_vlg&s","is_correct":False},
        {"name":"Bagels with Lox","image":"https://dempsters.ca/sites/default/files/styles/recipes_full_467x341_/public/2021-02/Lox%20Cream%20Cheese%20Bagel-061_1800x750-min.jpg?itok=o1vyYifd","is_correct":False}
    ]}
]

# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/learn/<int:lesson_id>')
def learn(lesson_id):
    # TODO: load whatever data you need for lesson #lesson_id
    return render_template('learn.html', lesson_id=lesson_id)


@app.route('/get_borough/<borough>')
def get_borough(borough):
    return jsonify(boroughs_data.get(borough, []))

@app.route('/quiz')
def quiz():
    saved = session.get('quiz_state', {})
    return render_template(
        'quiz.html',
        questions=quiz_questions,
        saved_answers=saved.get('answers', {}),
        saved_last=saved.get('last_question', 1)
    )

@app.route('/get_state')
def get_state():
    return jsonify(session.get('quiz_state', {'answers': {}, 'last_question': 1}))

@app.route('/save_state', methods=['POST'])
def save_state():
    data = request.get_json() or {}
    session['quiz_state'] = {
        'answers': data.get('answers', {}),
        'last_question': data.get('last_question', 1)
    }
    session.modified = True
    return jsonify(status='ok')

# Accept GET so front‐end redirect works
@app.route('/submit_quiz', methods=['GET', 'POST'])
def submit_quiz():
    return redirect(url_for('results'))

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/results')
def results():
    state   = session.get('quiz_state', {})
    answers = state.get('answers', {})
    score   = 0
    feedback = []

    for q in quiz_questions:
        qid  = q['id']
        user = answers.get(qid, '(No answer)')

        # compute correct answer
        if q['type'] == 'drag_and_drop':
            correct = next(opt['name'] for opt in q['options'] if opt['is_correct'])
        else:
            correct = q['correct']

        is_correct = (user == correct)
        if is_correct:
            score += 1

        entry = {
            'id':         qid,
            'num':        int(qid[1:]),
            'type':       q['type'],
            'text':       q['text'],
            'user':       user,
            'correct':    correct,
            'is_correct': is_correct
        }

        if q['type'] == 'drag_and_drop':
            entry['map_url']  = q['image']
            correct_opt      = next(opt for opt in q['options'] if opt['is_correct'])
            entry['dish_url'] = correct_opt['image']

        feedback.append(entry)

    return render_template(
        'results.html',
        score=score,
        total=len(quiz_questions),
        feedback=feedback
    )

@app.route('/reset_quiz')
def reset_quiz():
    # clear out any saved answers
    session.pop('quiz_state', None)
    # then send them into the quiz at Q1
    return redirect(url_for('quiz'))


@app.route('/reset_home')
def reset_home():
    # clear out any saved answers
    session.pop('quiz_state', None)
    # then send them to your homepage
    return redirect(url_for('home'))


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
