export interface DecodedResponse {
  name: string;
  picture: string;
  sub: string;
}

export interface User {
  _id: string;
  _type: string;
  userName: string;
  image: string;
}

export const userQuery = (userId: string) => {
  const query = `*[_type == "user" && _id == '${userId}']`;
  return query;
};
