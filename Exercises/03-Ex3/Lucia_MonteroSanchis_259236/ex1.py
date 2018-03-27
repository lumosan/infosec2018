
##############################
# First part
##############################

import pandas as pd

col_names = {"imdb": ["email", "movie", "date", "rating"],
    "dedis": ["salted-email", "salted-movie", "date", "rating"]}

lu_email = "lucia.monterosanchis@epfl.ch"

data = {}
for i in range(1,4):
    for ds in ["dedis", "imdb"]:
        name = "{}-{}".format(ds, i)
        data[name] = pd.read_csv("hw3_ex1_{}/{}.csv".format(lu_email, name),
            skipinitialspace=True, quotechar='"', names=col_names[ds])

data_i = data["imdb-1"].copy()
data_d = data["dedis-1"].copy()
movies = {}  # Dictionary with salted and unsalted movies
emails = {}  # Dictionary with salted and unsalted emails

# 1. Group imdb data by email
grouped_i = data_i.groupby("email")

# 2. Group dedis data by salted email
grouped_d = data_d.groupby("salted-email")

# 3. Iterate over each unique salted email in dedis, and unique email in imdb
seen_emails = []  # to check if there are duplicates!
for g_d in grouped_d:
    # get set of dates
    dates_d = set(g_d[1]["date"])
    for g_i in grouped_i:
        # get set of dates
        dates_i = set(g_i[1]["date"])
        # 3.1 check if the imdb dates is subset of dedis dates
        if dates_i.issubset(dates_d):
            # they're the same user!
            seen_emails.append(g_i[0])  # to check if there are duplicates
            # 3.2 add email and salted email to dictionary
            emails[g_i[0]] = g_d[0]
            # 3.3 join on date to get salted movie names related to unsalted
            combined_df = g_d[1].join(g_i[1].set_index(g_i[1]["date"]),
                on="date", how="inner", lsuffix='_left', rsuffix='_right')
            # 3.4 update the movies dictionary with the new findings
            movies.update(dict(zip(combined_df["salted-movie"],
                combined_df["movie"])))

# just in case...
if(len(seen_emails) - len(set(seen_emails))):
    print("There were duplicates!!!")

# 4. Save file with my movie ratings
f = open('solutions/1a.txt','w')
for m in grouped_d.get_group(emails[lu_email])["salted-movie"]:
    f.write(movies[m])
    f.write('\n')
f.close()



##############################
# Second part
##############################

data_i = data["imdb-2"].copy()
data_d = data["dedis-2"].copy()

def update(dictionary, k, v):
    """Function used to add a new sample to an existing dictionary.
    If key k is already defined it appends value v to k's list
    If key k is not defined, associates it with a singleton list
        containing v.
    """
    if k in dictionary.keys():
        dictionary[k].append(v)
    else:
        dictionary[k] = [v]

# 1. Group imdb data by movie and by email
grouped_u_i = data_i.groupby("email")
grouped_m_i = data_i.groupby("movie")

# 2. Group dedis data by salted movie and by email
grouped_u_d = data_d.groupby("salted-email")
grouped_m_d = data_d.groupby("salted-movie")

# 3. Create dictionary mapping movie names and freqs of appearance
count_m_i = grouped_m_i['email'].count().to_dict()
count_m_d = grouped_m_d['salted-email'].count().to_dict()

# 4. Sort dictionaries by freqs of appearance and do the mapping
import operator
sorted_i = sorted(count_m_i.items(), key=operator.itemgetter(1))
sorted_d = sorted(count_m_d.items(), key=operator.itemgetter(1))

movies = {ed[0]: ei[0] for (ei, ed) in zip(sorted_i, sorted_d)}

# 5. Iterate over each unique salted email in dedis, and unique email in imdb
emails = {}
for g_d in grouped_u_d:
    movies_d = set(g_d[1]["salted-movie"])
    movies_d_unsalted = {movies[m] for m in movies_d}
    for g_i in grouped_u_i:
        movies_i = set(g_i[1]["movie"])
        # 5.1 check if imdb movies is subset of dedis movies
        if movies_i.issubset(movies_d_unsalted):
            # 5.2 add email and salted email to dictionary
            update(emails, g_i[0], g_d[0])

# 6. Save file with my movie ratings
f = open('solutions/1b.txt','w')
for m in grouped_u_d.get_group(emails[lu_email][0])["salted-movie"]:
    f.write(movies[m])
    f.write('\n')
f.close()



##############################
## Third part
##############################

import pandas as pd

col_names = {"imdb": ["email", "movie", "date", "rating"],
    "dedis": ["salted-email", "salted-movie", "date", "rating"]}

lu_email = "lucia.monterosanchis@epfl.ch"

data = {}
for i in range(1,4):
    for ds in ["dedis", "imdb"]:
        name = "{}-{}".format(ds, i)
        data[name] = pd.read_csv("hw3_ex1_{}/{}.csv".format(lu_email, name),
            skipinitialspace=True, quotechar='"', names=col_names[ds])

data_i = data["imdb-3"].copy()
data_d = data["dedis-3"].copy()

def update(dictionary, k, v):
    """Function used to add a new sample to an existing dictionary.
    If key k is already defined it appends value v to k's list
    If key k is not defined, associates it with a singleton list
        containing v.
    """
    if k in dictionary.keys():
        dictionary[k].append(v)
    else:
        dictionary[k] = [v]

# 1. Group imdb data by movie and by email
grouped_u_i = data_i.groupby("email")
grouped_m_i = data_i.groupby("movie")

# 2. Group dedis data by salted movie and by email
grouped_u_d = data_d.groupby("salted-email")
grouped_m_d = data_d.groupby("salted-movie")

# 3.1 Define function for next step
def check_dates(dates_i, dates_d):
    """Iterates over dates_i and dates_d.
    Checks if for each d_i in dates_i there is at least one
    date in dates_d so that both are within 14 days.
    """
    for d_i in dates_i:
        if not find_close_date(d_i, dates_d):
            return False
    else:
        return True

def make_date(d, separator="/"):
    """Transform string into date object"""
    from datetime import date
    d_v = d.split(separator)
    return date(int('20'+d_v[2]), int(d_v[1]), int(d_v[0]))

def find_close_date(d_i, dates_d, close=14):
    """Returns True if theres a date close to d_i in dates_d"""
    f_d_i = make_date(d_i)
    for d_d in dates_d:
        f_d_d = make_date(d_d)
        delta = f_d_i - f_d_d
        if abs(delta.days) <= close:
            return True
    else:
        return False

# 3.2 Iterate over each salted movie in dedis, and movie in imdb
# creating a dictionary of movie and hashed movie pairs
movies = {}
missing_movies = []
for g_i in grouped_m_i:
    dates_i = g_i[1]["date"]
    for g_d in grouped_m_d:
        dates_d = g_d[1]["date"]
        if check_dates(dates_i, dates_d):
            movies[g_d[0]] = g_i[0]
            break
    else:
        missing_movies.append(g_i[0])

# 3.3 Get the hashed titles for the missing movies
missing_salted_movies = [g_d[0] for g_d in grouped_m_d
    if g_d[0] not in movies.keys()]

# 4 Get the missing movies
# 4.1 Find user movies
movies_d_unsalted = []
u_movies = {}
emails = {}
for g_i in grouped_u_i:
    movies_i = set(g_i[1]["movie"])
    for g_d in grouped_u_d:
        movies_d = list(g_d[1]["salted-movie"])
        movies_d_unsalted = [movies[m] for m in movies_d if m in movies]
        if movies_i.issubset(movies_d_unsalted):
            emails[g_d[0]] = g_i[0]
            if (len(movies_d_unsalted) - len(movies_d)):
                u_movies[g_d[0]] = set(movies_d) - set(movies.keys())

# 4.2 try with the users we mapped
for m in missing_movies:
    for h_m in missing_salted_movies:
        for h_e, e in emails.items():
            gd = grouped_u_d.get_group(h_e)["salted-movie"]
            if h_m in list(gd):
                gi = grouped_u_i.get_group(e)["movie"]
                if m in list(gi):
                    print(":)")

# 4.3 The previous didn't work! need to map some more users...
users_list = list([g[0] for g in grouped_u_i if g[0] not in emails.values()])
h_users_list = list([g[0] for g in grouped_u_d if g[0] not in emails])

# 4.3.1 I'll keep only the ones who voted some missing movie
users_list_= [u for u in users_list if missing_movies[0]
    in list(grouped_u_i.get_group(u)["movie"])]

# 4.3.2 and I remove the ones who also voted the other missing movie
users_list = [u for u in users_list_ if missing_movies[1]
    not in list(grouped_u_i.get_group(u)["movie"])]

# 4.3.3 and I do the same with the dedis data
h_users_list_ = [u for u in h_users_list if missing_salted_movies[0]
    in list(grouped_u_d.get_group(u)["salted-movie"])]

h_users_list_0 = [u for u in h_users_list_ if missing_salted_movies[1]
    not in list(grouped_u_d.get_group(u)["salted-movie"])]

h_users_list_ = [u for u in h_users_list if missing_salted_movies[1]
    in list(grouped_u_d.get_group(u)["salted-movie"])]

h_users_list_1 = [u for u in h_users_list_ if missing_salted_movies[0]
    not in list(grouped_u_d.get_group(u)["salted-movie"])]

# 4.3.4 now I try to map someone in h_users_list_0
# with someone in users_list
inv_movies = {v: k for k, v in movies.items()}

h_candidate = h_users_list_0[0]
h_movies_cand = grouped_u_d.get_group(h_candidate)
c_dates_0 = {}

for c_i in users_list:
    movies_cand = grouped_u_i.get_group(c_i)
    x = [inv_movies[m] in list(h_movies_cand["salted-movie"]) for m in movies_cand["movie"]
        if m in inv_movies]
    c_dates_0[c_i] = x.count(True) / (x.count(True) + x.count(False))

# I keep the best mapping for h_users_list_0
import operator
max_arg_0 = max(c_dates_0.items(), key=operator.itemgetter(1))[0]
print("{}: {}".format(max_arg_0, c_dates_0[max_arg_0]))

# 4.3.5 now I try to map someone in h_users_list_1
# with someone in users_list
inv_movies = {v: k for k, v in movies.items()}

h_candidate = h_users_list_1[0]
h_movies_cand = grouped_u_d.get_group(h_candidate)
c_dates_1 = {}

for c_i in users_list:
    movies_cand = grouped_u_i.get_group(c_i)
    x = [inv_movies[m] in list(h_movies_cand["salted-movie"]) for m in movies_cand["movie"]
        if m in inv_movies]
    c_dates_1[c_i] = x.count(True) / (x.count(True) + x.count(False))

# I keep the best mapping for h_users_list_1
max_arg_1 = max(c_dates_1.items(), key=operator.itemgetter(1))[0]
print("{}: {}".format(max_arg_1, c_dates_1[max_arg_1]))

# 4.3.6 I compare the results for the two best mappings I got before

candidate = None

if c_dates_0[max_arg_0] > c_dates_1[max_arg_1]:
    candidate = max_arg_0
else:
    candidate = max_arg_1

# I was able to match Jeremy.Corcoba@unil.ch!

# 4.4 Now I use his ratings to find the missing matches and
# add the found movie to 'movies'
movies[[hm for hm in grouped_u_d.get_group(h_candidate)["salted-movie"]
    if hm not in movies][0]] = [m for m in grouped_u_i.get_group(candidate)["movie"]
    if m not in inv_movies][0]

movies[[hm for hm in missing_salted_movies if hm not in movies.keys()][0]] = [m
    for m in missing_movies if m not in movies.values()][0]

# 5 Find my movies
movies_d_unsalted = []
movies_i = set(grouped_u_i.get_group(lu_email)["movie"])
lu_movies_salted = []
lu_movies = []
for g_d in grouped_u_d:
    movies_d = g_d[1]["salted-movie"]
    movies_d_unsalted = {movies[m] for m in movies_d if m in movies}
    if movies_i.issubset(movies_d_unsalted):
        lu_movies = movies_d_unsalted
        lu_movies_salted = movies_d
        if not len(lu_movies) == len(lu_movies_salted):
            print("{} movie(s) missing!".format(len(lu_movies_salted) - len(lu_movies)))

# 6 Save file with my movie ratings
f = open('solutions/1c.txt','w')
for m in lu_movies:
    f.write(m)
    f.write('\n')
f.close()