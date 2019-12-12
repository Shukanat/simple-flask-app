import pandas as pd
import seaborn as sns
import io
import matplotlib.pyplot as plt
import base64
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired
plt.rcParams["figure.figsize"] = (6,6)
plt.gcf().subplots_adjust(bottom=0.40)

def get_data(cnx):
    
        
    query = """ SELECT CAST(name AS VARCHAR) AS movie, ROUND(SUM(

                CASE 
                    WHEN CAST(gender AS VARCHAR) = 'F' THEN 1.0
                    ELSE 0
                    
                END) / COUNT(actor_id), 2) AS proportion_female 
                       
            FROM (
            
                SELECT T1.movie_id, M.name, T1.actor_id, CONCAT(A.first_name, ' ', A.last_name) AS full_name, A.gender, M.rank

                FROM
                    (SELECT movie_id, actor_id 
                    FROM analysis_roles) T1
                    JOIN analysis_movies M ON T1.movie_id = M.id
                    JOIN analysis_actors A ON T1.actor_id = A.id

                WHERE M.rank >= 8) AS Subquery
            
            GROUP BY CAST(name AS VARCHAR)
            ORDER BY proportion_female DESC
        """
    
    df = pd.read_sql(query, cnx)
    
    return df

def do_plot(df):
    ax = sns.barplot(x="movie", y="proportion_female", data=df)
    for item in ax.get_xticklabels():
        item.set_rotation(90)
    
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    graph = base64.b64encode(bytes_image.getvalue()).decode()
    plt.close()
    return f'data:image/png;base64,{graph}'

class graph_request(FlaskForm):
    year = IntegerField('Choisissez une année', validators=[DataRequired()])
    submit = SubmitField('Go!')
    
def genre_by_year(year, cnx):
    query = f"""SELECT * 
    FROM analysis_movies A
    JOIN analysis_movies_genres B ON CAST(A.id as VARCHAR) = CAST(B.movie_id AS VARCHAR) 
    WHERE year={year} 
    ORDER BY CAST(name as VARCHAR(50))"""
    
    df = pd.read_sql(query, cnx)
    
    return df

def get_countplot(df, year):
    ax = sns.countplot(y='genre', data=df)
    ax.set_title("Les plus populaires genres de films pour l'année: {}".format(year))
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    graph = base64.b64encode(bytes_image.getvalue()).decode()
    plt.close()
    return f'data:image/png;base64,{graph}'