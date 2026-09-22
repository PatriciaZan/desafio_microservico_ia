
# para limpar espaçamentos, da para add mais coisas/validações depois
# Faz sentido mudar para lowerCasa? E se eu quiser a resposta original depois, ai teria de criar outro campo no json para guardas as duas versões?
# Ou em memória

def clean_text(value: str | None) -> str:
    if not value:
        return ""

    return " ".join(value.split())