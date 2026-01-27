from django import template

register = template.Library()

"""
    title: Título do card
    img_url: URL da imagem
    subtitle: Subtitulo do card
    time_value: Mostrar horário
    time_rating: Mostrar rating
    rating_value: Valor da avaliação
    time_start: Horário de início
    time_end: Horário de término
    day_text: Texto do status do dia
    color_status: Cor do status (green, red)
    btn_text_conclude: Texto do botão de conclusão
    btn_color_conclude: Cor do botão (green, red)
    buttons_preset: Lista de botões de finalização
"""
@register.inclusion_tag('components/card_wonder.html')
def card_wonder(
        title="",
        img_url="",
        subtitle="",
        time_value="",
        time_rating=False,
        rating_value="",
        time_start="",
        time_end="",
        day_text="",
        color_status="green",
        btn_text_conclude="",
        btn_color_conclude="green",
        buttons_preset="",
        **kwargs
):
    button_presets = {
        'finish_cancel': [
            {'text': 'Finalizar', 'color': 'blue'},
            {'text': 'Cancelar', 'color': 'red'},
        ],
        'edit_delete': [
            {'text': 'Editar', 'color': 'blue'},
            {'text': 'Excluir', 'color': 'red'},
        ],
        'view_refuse': [
            {'text': 'Ver detalhes', 'color': 'blue'},
            {'text': 'Recusar', 'color': 'red'},
        ],
        'confirm_reject': [
            {'text': 'Confirmar', 'color': 'green'},
            {'text': 'Recusar', 'color': 'red'},
        ],
    }

    btn_finish = button_presets.get(buttons_preset)

    return {
        'title': title,
        'img_url': img_url,
        'subtitle': subtitle,
        'time_value': time_value,
        'time_rating': time_rating,
        'rating_value': rating_value,
        'time_start': time_start,
        'time_end': time_end,
        'day_text': day_text,
        'color_status': color_status,
        'btn_text_conclude': btn_text_conclude,
        'btn_color_conclude': btn_color_conclude,
        'btn_finish': btn_finish,
        **kwargs
    }