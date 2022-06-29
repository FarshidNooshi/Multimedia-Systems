from .utils.log_business import MyLogger


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __str__(self):
        return f"{self.char}:{self.freq}"

    def __repr__(self):
        return f"{self.char}:{self.freq}"


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
            node = Node(char, freq)
            nodes.append(node)
        nodes.sort(key=lambda x: x.freq)
        while len(nodes) > 1:
            node1 = nodes.pop(0)
            node2 = nodes.pop(0)
            node3 = Node(None, node1.freq + node2.freq)
            node3.left = node1
            node3.right = node2
            nodes.append(node3)
            nodes.sort(key=lambda x: x.freq)
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
        if tree.char is not None:
            if char == '0':
                return self.encode(tree.left, char)
            else:
                return self.encode(tree.right, char)
        else:
            return tree.char  #  ''

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
        if tree.char is None:
            if code[0] == '0':
                return self.decode(tree.left, code[1:])
            else:
                return self.decode(tree.right, code[1:])
        else:
            return tree.char

    def encode_file(self, filepath, output_filepath):
        """
        Encodes a file using a tree

            Parameters
            ----------
                filepath : str
                    filepath of the file to encode
                output_filepath : str
                    filepath of the output file
        """
        self.logger.info('encoding file')
        with open(filepath, 'r') as f:
            text = f.read()
        freq_dict = {}
        for char in text:
            if char in freq_dict:
                freq_dict[char] += 1
            else:
                freq_dict[char] = 1
        tree = self.create_tree(freq_dict)
        encoded_text = ''
        for char in text:
            encoded_text += self.encode(tree, char)
        with open(output_filepath, 'w') as f:
            f.write(encoded_text)
        self.logger.info('file encoded')

