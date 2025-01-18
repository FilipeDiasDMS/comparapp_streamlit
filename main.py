import streamlit as st
import tempfile
import matplotlib.pyplot as plt
import os

plt.switch_backend('Agg')

project_dir = os.path.dirname(os.path.abspath(__file__))
temp_images_dir = os.path.join(project_dir, 'temp_images')
os.makedirs(temp_images_dir, exist_ok=True)
tempfile.tempdir = temp_images_dir


# Função para criar o gráfico
def create_plot(result_1_value, result_2_value):
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    ax.bar([1, 2], [result_1_value, result_2_value], tick_label=["Produto 1", "Produto 2"],
           color=['#bc8d27', '#976f17'])
    ax.set_xticks([1, 2])
    ax.set_xticklabels(["Produto 1", "Produto 2"], fontsize=15, color='white')
    ax.get_yaxis().set_visible(False)
    ax.tick_params(axis='y', labelcolor='white')

    for spine in ax.spines.values():
        spine.set_visible(False)

    img_path = os.path.join(temp_images_dir, 'plot_{}.png'.format(os.urandom(6).hex()))
    plt.savefig(img_path, format='png')

    plt.close(fig)
    return img_path


# Função para calcular o preço por grama do produto 1
def calcular1(pr1, ps1):
    try:
        price = float(pr1)
        peso = float(ps1)
        resultado1 = price / peso
        return resultado1
    except ValueError:
        return None


# Função para calcular o preço por grama do produto 2
def calcular2(pr2, ps2):
    try:
        price2 = float(pr2)
        peso2 = float(ps2)
        resultado2 = price2 / peso2
        return resultado2
    except ValueError:
        return None


# Função para comparar os preços e gerar o gráfico
def compara(pr1, ps1, pr2, ps2):
    if not pr1 or not ps1 or not pr2 or not ps2:
        return None, "Insira informações válidas"
    resultado1 = calcular1(pr1, ps1)
    resultado2 = calcular2(pr2, ps2)

    if resultado1 is None or resultado2 is None:
        return None, "Valores inválidos"

    if resultado2 > resultado1:
        display_final = f'O produto 1 está mais barato'
    elif resultado2 == resultado1:
        display_final = f'Ambos custam o mesmo'
    else:
        display_final = f'O produto 2 está mais barato'

    return (resultado1, resultado2), display_final


# Função para calcular a diferença percentual
def calcular_diferenca(result_1, result_2):
    try:
        dif = result_1 - result_2
        dif_porc = dif * 1000
        return f'A diferença é de {abs(dif_porc):.2f}%'
    except ValueError:
        return 'Valores inválidos'


# Layout da aplicação no Streamlit
def main():
    st.title('Comparador de preços')

    # Entradas de dados
    pr1 = st.text_input('Preço (R$) do produto 1')
    ps1 = st.text_input('Peso (g) do produto 1')
    pr2 = st.text_input('Preço (R$) do produto 2')
    ps2 = st.text_input('Peso (g) do produto 2')

    result_1, result_2 = None, None

    # Botão para comparar e calcular
    if st.button('Calcular'):
        resultados, mensagem = compara(pr1, ps1, pr2, ps2)

        if resultados:
            result_1, result_2 = resultados
            st.write(f"Resultado 1 (R$/g): {result_1:.3f}")
            st.write(f"Resultado 2 (R$/g): {result_2:.3f}")

            # Exibir diferença percentual
            diferenca = calcular_diferenca(result_1, result_2)
            st.write(diferenca)
        else:
            st.write(mensagem)

    def reset_fields():
        st.session_state.pr1 = ''
        st.session_state.ps1 = ''
        st.session_state.pr2 = ''
        st.session_state.ps2 = ''
        st.session_state.resultados = None
        st.session_state.mensagem = ''

    # Gerar gráfico somente se houver resultados válidos
    if result_1 is not None and result_2 is not None:
        img_path = create_plot(result_1, result_2)
        st.image(img_path)



if __name__ == '__main__':
    main()

