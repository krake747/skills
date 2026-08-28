import { db } from "../db";

export async function getUser(id: string) {
  const user = await db.users.findById(id);
  if (!user) return { status: 404, body: { error: "User not found" } };
  return { status: 200, body: user };
}
