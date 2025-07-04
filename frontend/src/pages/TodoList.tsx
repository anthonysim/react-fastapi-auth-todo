import { useState } from "react";

interface Todo {
  id: number;
  title: string;
  description: string;
}

export default function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([
    { id: 1, title: "Buy groceries", description: "Milk, Bread, Eggs" },
    { id: 2, title: "Workout", description: "Run 30 minutes" },
  ]);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editedTitle, setEditedTitle] = useState("");
  const [editedDesc, setEditedDesc] = useState("");

  const startEdit = (todo: Todo) => {
    setEditingId(todo.id);
    setEditedTitle(todo.title);
    setEditedDesc(todo.description);
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditedTitle("");
    setEditedDesc("");
  };

  const saveEdit = (id: number) => {
    setTodos((prev) =>
      prev.map((todo) =>
        todo.id === id
          ? { ...todo, title: editedTitle, description: editedDesc }
          : todo
      )
    );
    cancelEdit();
  };

  const deleteTodo = (id: number) => {
    setTodos((prev) => prev.filter((todo) => todo.id !== id));
  };

  return (
    <div className="min-h-screen p-10 text-white bg-gray-950">
      <div className="max-w-6xl mx-auto">
        <h1 className="mb-6 text-3xl font-bold text-center">Todo Grid</h1>

        {/* Grid Header */}
        <div className="grid grid-cols-3 gap-2 p-3 text-sm font-semibold bg-gray-800 border-b border-gray-700 rounded-t-lg">
          <div>Title</div>
          <div>Description</div>
          <div className="text-center">Actions</div>
        </div>

        {/* Grid Rows */}
        {todos.map((todo) => (
          <div
            key={todo.id}
            className="grid items-center grid-cols-3 gap-2 p-3 bg-gray-900 border-b border-gray-800 hover:bg-gray-850"
          >
            {editingId === todo.id ? (
              <>
                <input
                  className="p-2 text-white bg-gray-800 border border-gray-700 rounded"
                  value={editedTitle}
                  onChange={(e) => setEditedTitle(e.target.value)}
                />
                <input
                  className="p-2 text-white bg-gray-800 border border-gray-700 rounded"
                  value={editedDesc}
                  onChange={(e) => setEditedDesc(e.target.value)}
                />
                <div className="flex justify-center gap-2">
                  <button
                    onClick={() => saveEdit(todo.id)}
                    className="px-3 py-1 bg-green-600 rounded hover:bg-green-700"
                  >
                    Save
                  </button>
                  <button
                    onClick={cancelEdit}
                    className="px-3 py-1 bg-gray-600 rounded hover:bg-gray-700"
                  >
                    Cancel
                  </button>
                </div>
              </>
            ) : (
              <>
                <div>{todo.title}</div>
                <div>{todo.description}</div>
                <div className="flex justify-center gap-2">
                  <button
                    onClick={() => startEdit(todo)}
                    className="px-3 py-1 bg-blue-600 rounded hover:bg-blue-700"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => deleteTodo(todo.id)}
                    className="px-3 py-1 bg-red-600 rounded hover:bg-red-700"
                  >
                    Delete
                  </button>
                </div>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
