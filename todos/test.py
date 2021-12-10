from metacity.core.styles.apply import parse 


style = """
@layer ("Využití") {
    @color: #000000;

    @meta(CTVUK_POPI) {
        "komunikace - silnice": #FFFFFF;
        "komunikace - chodník nebo parková cesta": #EEEEEE;
        "zeleň v zástavbě - veřejná zeleň": #00FF00;
        "vodní plochy - řeka, potok": #8888FF;
        "železnice": #FF0000;
    }
}
"""

while True:
    parse(style)
