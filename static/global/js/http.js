const http = axios.create({
  baseURL: '/api/',
  headers: {
      'Content-Type': 'application/json'
  }
})

const request = async args => {
  let response
  const csrftoken = $('input[name="csrfmiddlewaretoken"]').attr('value')
  http.defaults.headers['X-CSRFToken'] = csrftoken
  switch (args['method']) {
    case 'post':
      try {
        response = await http.post(args['url'], args['data'])
        return response
      } catch (error) {
        return error
      }
    case 'get':
      try {
        response = await http.get(args['url'])
        return response
      } catch (error) {
        return error
      }
    case 'patch':
      try {
        response = await http.patch(args['url'], args['data'])
        return response
      } catch (error) {
        return error
      }
    default:
      return false
  }
}
