class SnakeAndCamelCaseConvertor():
    
    @staticmethod
    def snack_to_camel(data):
        result = {}
        for key, value in data.items():
            if(key == 'data'):
                if(isinstance(value, list)):
                    response_data = []
                    for data2 in value:
                        result2 = {}
                        for key2, value2 in data2.items():
                            words = key2.split('_')
                            camelcase_key = words[0] + ''.join(word.title() for word in words[1:])
                            result2[camelcase_key] = value2
                        response_data.append(result2)
                    result['data'] = response_data
                    continue
                elif(value is not None):
                    result2 = {}
                    for key2, value2 in value.items():
                        words = key2.split('_')
                        camelcase_key = words[0] + ''.join(word.title() for word in words[1:])
                        result2[camelcase_key] = value2
                    result['data'] = result2
                    continue

            words = key.split('_')
            camelcase_key = words[0] + ''.join(word.title() for word in words[1:])
            result[camelcase_key] = value
        return result