# flake8: noqa
import click

from moic.config import console


@click.command()
def rabbit():
    """Print an amazing rabbit"""
    funny_rabbit = """
              /|      __
             / |   ,-~ /
            Y :|  //  /
            | jj /( .^
             >-\"~\"-v\"
            /       Y
           jo  o    |
          ( ~T~     j    Hello !
           >._-' _./
          /   \"~\"  |
         Y     _,  |
        /| ;-\"~ _  l
       / l/ ,-\"~    \\
       \\//\\/      .- \\
        Y        /    Y
        l       I     !
        ]\      _\    /\"\\
       (\" ~----( ~   Y.  )
    """

    console.print(funny_rabbit)
