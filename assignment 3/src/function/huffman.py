from .utils.log_business import MyLogger


class Node:
    def __init__(self, symbol, freq):
        """
        Initializes a node with a character and frequency

            Parameters
            ----------
                symbol : set of str
                    set of symbols of the node`s children
                freq : double
                    frequency of the character
        """
        self.symbols = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __str__(self):
        return f"{self.symbols}:{self.freq}"

    def __repr__(self):
        return f"{self.symbols}:{self.freq}"


class Huffman:
    def __init__(self, log_path):
        self.logger = MyLogger('assignment3.function.huffman', log_path)

    def create_tree(self, freq_dict):
        """
        Creates a tree from a dictionary of characters and their frequencies

            Parameters
            ----------
                freq_dict : dict
                    dictionary of characters and their frequencies

            Returns
            -------
                out : :py:class:`Node`
                    root node of the tree
        """
        self.logger.info('creating tree')
        nodes = []
        for char, freq in freq_dict.items():
            nodes.append(Node({char}, freq))
        self.logger.debug('nodes list created')
        nodes.sort(key=lambda x: x.freq)
        self.logger.debug('ready to create tree')
        while len(nodes) > 1:
            node1 = nodes.pop(0)
            node2 = nodes.pop(0)
            node3 = Node(node1.symbols.union(node2.symbols), node1.freq + node2.freq)
            node3.left = node1
            node3.right = node2
            nodes.append(node3)
            nodes.sort(key=lambda x: x.freq)
        self.logger.debug('tree created')
        return nodes[0]

    def encode(self, tree, char):
        """
        Encodes a character using a tree

            Parameters
            ----------
                tree : :py:class:`Node`
                    root node of the tree
                char : str
                    character to encode

            Returns
            -------
                out : str
                    encoded character
        """
        if tree.symbols is not None:
            if char in tree.left.symbols:
                return '0' + self.encode(tree.left, char)
            elif char in tree.right.symbols:
                return '1' + self.encode(tree.right, char)
            else:
                self.logger.error(f'character {char} not in tree')
                raise ValueError(f'{char} not in tree')
        else:
            return ''

    def decode(self, tree, code):
        """
        Decodes a code using a tree

            Parameters
            ----------
                tree : :py:class:`Node`
                    root node of the tree
                code : str
                    code to decode

            Returns
            -------
                out : str
                    decoded character
        """
        if tree.symbols is None:
            if code[0] == '0':
                return self.decode(tree.left, code[1:])
            else:
                return self.decode(tree.right, code[1:])
        else:
            return tree.symbols

    def encode_array(self, array):
        """
        Encodes an array of characters using a tree

            Parameters
            ----------
                array : list of str
                    list of characters to encode

            Returns
            -------
                out : dict
                    dictionary of characters and their encoded codes
        """
        self.logger.info('encoding array')
        freq_dict = {}
        for char in array:
            if char in freq_dict:
                freq_dict[char] += 1
            else:
                freq_dict[char] = 1
        self.logger.debug('frequency dictionary created')
        tree = self.create_tree(freq_dict)
        self.logger.debug('tree created')
        encoded_dict = {}
        for char in freq_dict:
            encoded_dict[char] = self.encode(tree, char)
        self.logger.debug('encoded dictionary created')
        return encoded_dict
