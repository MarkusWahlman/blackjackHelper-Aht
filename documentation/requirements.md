Vaatimusmäärittely kannattaa yleensä aloittaa tunnistamalla järjestelmän erityyppiset käyttäjäroolit. Sovelluksellamme ei ole toistaiseksi muuta kuin normaaleja käyttäjiä. Jatkossa sovellukseen saatetaan lisätä myös ylläpitäjän oikeuksilla varustettu käyttäjärooli.

Kun sovelluksen käyttäjäroolit ovat selvillä, mietitään mitä toiminnallisuuksia kunkin käyttäjäroolin halutaan pystyvän tekemään sovelluksen avulla.

Todo-sovelluksen normaalien käyttäjien toiminnallisuuksia ovat esim. seuraavat

    käyttäjä voi luoda järjestelmään käyttäjätunnuksen
    käyttäjä voi kirjautua järjestelmään
    kirjautumisen jälkeen käyttäjä näkee omat tekemättömät työt eli todot
    käyttäjä voi luoda uuden todon
    käyttäjä voi merkitä todon tehdyksi, jolloin todo häviää listalta

Ylläpitäjän toiminnallisuuksia voisivat olla esim. seuraavat

    ylläpitäjä näkee tilastoja sovelluksen käytöstä
    ylläpitäjä voi poistaa normaalin käyttäjätunnuksen

Ohjelmiston vaatimuksiin kuuluvat myös toimintaympäristön rajoitteet. Todo-sovellusta koskevat seuraavat rajoitteet

    ohjelmiston tulee toimia Linux- ja OSX-käyttöjärjestelmillä varustetuissa koneissa
    käyttäjien ja todojen tiedot talletetaan paikallisen koneen levylle

Vaatimusmäärittelyn aikana hahmotellaan yleensä myös sovelluksen käyttöliittymä.

Voit myös tehdä referenssiprojektin tapaan käyttöliittymäluonnoksen, se ei ole kuitenkaan pakollinen.

ESIM:
Sovelluksen tarkoitus
.............

Perusversion tarjoama toiminnallisuus
Ennen kirjautumista

    Käyttäjä voi luoda järjestelmään käyttäjätunnuksen
        Käyttäjätunnuksen täytyy olla uniikki ja pituudeltaan vähintään 3 merkkiä
    Käyttäjä voi kirjautua järjestelmään
        Kirjautuminen onnistuu syötettäessä olemassaoleva käyttäjätunnus ja salasana kirjautumislomakkeelle
        Jos käyttäjää ei olemassa, tai salasana ei täsmää, ilmoittaa järjestelmä tästä

Kirjautumisen jälkeen

    Käyttäjä näkee omat tekemättömät työt eli todot
    Käyttäjä voi luoda uuden todon
        Luotu todo näkyy ainoastaan sen luoneelle käyttäjälle
    Käyttäjä voi merkitä todon tehdyksi, jolloin todo häviää listalta
    Käyttäjä voi kirjautua ulos järjestelmästä

Jatkokehitysideoita
Perusversion jälkeen järjestelmää täydennetään ajan salliessa esim. seuraavilla toiminnallisuuksilla:

    Tehdyksi merkittyjen todojen tarkastelu
    Tehdyksi merkittyjen todojen merkkaaminen tekemättömiksi
    Todon tietojen editointi
    Todojen järjestely tärkeysjärjestykseen
    Todojen määrittely muille käyttäjille
    Käyttäjätiimit, jotka näkevät kaikki yhteiset todot
    Mahdollisuus useampaan erilliseen todo-listaan
    Lisätään todoon kenttä, johon on mahdollista merkitä tarkempia todoon liittyviä tietoja
    Käyttäjätunnuksen (ja siihen liittyvien todojen) poisto
