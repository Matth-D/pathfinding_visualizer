import re
import sys

from pathfinder import ui

if __name__ == "__main__":
    ui.main()

# syntaxe pour executer un script dans le terminal avec des arguments

# if __name__ == "__main__":
#     sys.argv[0] = re.sub(r"(-script\.pyw?|\.exe)?$", "", sys.argv[0])
#     sys.exit(ui.main())
