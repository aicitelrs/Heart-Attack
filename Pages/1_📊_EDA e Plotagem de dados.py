import streamlit as st
import pandas as pd
import plotly.express as px


df = pd.read_csv('data/heart_disease.csv')
dfp = pd.read_parquet('data/heart_disease.parquet')

st.title('Análise exploratória dos dados e Plotagens')


def profilling():
     st.write('Inserir o Dicionário aqui talvez ??')
    
     st.subheader("Data Profilling")
    
     with st.expander('Proffiling De Dados'):
            
             # Carregar o conteúdo do arquivo HTML
         with open("data/eda.html", "r") as file:
                 pagina_html = file.read()

                 # Exibir o conteúdo HTML
         st.components.v1.html(pagina_html, height = 700, scrolling=True)

def parallel_cateogries():

    st.subheader('Categorias Paralelas')
    col1,col2=st.columns([.3,.7])
    with col1:
        nomes_colunas=['HeartDiseaseorAttack','HighBP','HighChol','CholCheck','BMI','Smoker','Stroke','Diabetes','PhysActivity','Fruits','Veggies','HvyAlcoholConsump',
                        'AnyHealthcare','NoDocbcCost','GenHlth','MentHlth','PhysHlth','DiffWalk','Sex','Income','Age','Education']
        colunas= col1.multiselect('Colunas',options=nomes_colunas)

        if len(colunas) >=2:
                grafico= px.parallel_categories(dfp[colunas])
                button_input= st.button('Gerar Gráfico')
                pronto = st.success('Gráfico Pronto Para Ser Gerado', icon='✅')
                if button_input:
                        with st.empty():
                             pronto.empty()
                        with col2:
                                col2.plotly_chart(grafico,use_container_width=True)         
        if len(colunas) <=1:
            st.error('Deve Haver no Mínimo Duas Colunas', icon='🚨')                    

def histograms():
    st.subheader('Histogramas')
    col1,col2=st.columns([.3,.7])
    with col1:
          nomes_colunas=['HeartDiseaseorAttack','HighBP','HighChol','CholCheck','BMI','Smoker','Stroke','Diabetes','PhysActivity','Fruits','Veggies','HvyAlcoholConsump',
                       'AnyHealthcare','NoDocbcCost','GenHlth','MentHlth','PhysHlth','DiffWalk','Sex','Income','Age','Education']
          colunas=col1.selectbox('Colunas', options=nomes_colunas, key='histograma')
          grafico= px.histogram(dfp,x=colunas, color='HeartDiseaseorAttack')
    with col2:
        col2.plotly_chart(grafico,use_container_width=True)
def boxplot():
    st.subheader("Gráfico de Caixa - Boxplot")
    col1,col2= st.columns([.3,.7])
    with col1:
          nomes_colunas=['HeartDiseaseorAttack','HighBP','HighChol','CholCheck','BMI','Smoker','Stroke','Diabetes','PhysActivity','Fruits','Veggies','HvyAlcoholConsump',
                       'AnyHealthcare','NoDocbcCost','GenHlth','MentHlth','PhysHlth','DiffWalk','Sex','Income','Age','Education']
          colunas=col1.selectbox('Colunas', options=nomes_colunas, key='boxplot')
          grafico= px.box(dfp, x=colunas)
    with col2:
        col2.plotly_chart(grafico,use_container_width=True)


def idade(df):
    bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, float('inf')]
    labels = ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49',
              '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80 ou mais']
    
    df['Age'] = pd.cut(df['Age'], bins=bins, labels=labels, right=True)

    return df

def bar_one():
    st.markdown('<h3>Gráfico de Barras </h3>', unsafe_allow_html=True)

    dfp['HeartDiseaseorAttack'] = dfp['HeartDiseaseorAttack'].astype('category')

    idade(dfp)

    binario_para_sim_nao(dfp)

    binario_para_genero(dfp)
    
    agrupando_idade = dfp.groupby(
        'Age')['HeartDiseaseorAttack'].value_counts().to_frame().reset_index()

    agrupando_idade.columns = ['Age', 'HeartDiseaseorAttack', 'Total']

    fig = px.bar(agrupando_idade, x="Age", y='Total',
                 color="HeartDiseaseorAttack", title="Gráfico Idade x Doença Cardíaca",
                 color_discrete_map={0: "#99ccff", 1: "red"})
    st.plotly_chart(fig)


def binario_para_sim_nao(df):
    colunas_binarias = [col for col in df.columns if (df[col].eq(0) | df[col].eq(1)).all() and col != 'Sex']

    mapeamento = {0: 'No', 1: 'Yes'}

    df[colunas_binarias] = df[colunas_binarias].map(
        lambda x: mapeamento.get(x, x))

    return df


def binario_para_genero(df):

    mapeamento = {0: 'Female', 1: 'Male'}

    df['Sex'] = df['Sex'].map(mapeamento)

    return df


def bar_two():
    st.markdown('<h3>Histograma</h3>', unsafe_allow_html=True)

    colunas_binarias = ['HighBP', 'HighChol', 'CholCheck', 'Smoker', 'Stroke', 'PhysActivity',
                        'Fruits', 'Veggies', 'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'DiffWalk']
    
    coluna = st.selectbox("Selecione uma coluna binária para visualização:",
                          options=colunas_binarias)

    if coluna:
        agrupando_por_sexo = dfp.groupby('Sex')[coluna].value_counts().to_frame().reset_index()
        agrupando_por_sexo.columns = ['Sexo', coluna, 'Total']
        
        fig = px.histogram(agrupando_por_sexo, x='Sexo', y='Total',
                        color=coluna, barmode='group',
                        color_discrete_map={0: 'lightgray', 1: 'royalblue'},
                        title = f'Gráfico de barras: agrupando por sexo',
                        labels={'Total': 'Número de Pessoas', coluna: coluna},
                        height=500)

        st.plotly_chart(fig)
    else:
        st.warning("Por favor, selecione uma coluna binária para visualização.")

def box_plot():
    fig = px.box(dfp, x='Sex', y='BMI')

    st.plotly_chart(fig)

def buildPage():
    profilling()
    parallel_cateogries()
    histograms()
    boxplot()
    bar_one()
    bar_two()
    box_plot()


if __name__ == '__main__':
    buildPage()


    