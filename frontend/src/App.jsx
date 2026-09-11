import { useEffect, useRef, useState } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'
const TOKEN_KEY = 'stoksmaster_token'

const emptyForm = {
  name: '',
  image: '',
  category: 'Outros',
  price: '',
  quantity: 0,
}

const categories = ['Bebidas', 'Alimentos', 'Limpeza', 'Higiene', 'Eletrônicos', 'Roupas', 'Casa', 'Pets', 'Outros']

function CategorySelect({ value, onChange }) {
  const [isOpen, setIsOpen] = useState(false)
  const [openUpward, setOpenUpward] = useState(false)
  const selectRef = useRef(null)

  useEffect(() => {
    const handleOutsideClick = (event) => {
      if (selectRef.current && !selectRef.current.contains(event.target)) setIsOpen(false)
    }
    document.addEventListener('mousedown', handleOutsideClick)
    return () => document.removeEventListener('mousedown', handleOutsideClick)
  }, [])

  const toggleOptions = () => {
    if (!isOpen && selectRef.current) {
      const bounds = selectRef.current.getBoundingClientRect()
      const availableBelow = window.innerHeight - bounds.bottom
      setOpenUpward(availableBelow < 300 && bounds.top > availableBelow)
    }
    setIsOpen((open) => !open)
  }

  return (
    <div className="category-select" ref={selectRef}>
      <button type="button" className="category-select-trigger" onClick={toggleOptions} aria-haspopup="listbox" aria-expanded={isOpen}>
        <span>{value}</span>
        <span className={`category-chevron ${isOpen ? 'category-chevron-open' : ''}`}>⌄</span>
      </button>
      {isOpen && (
        <div className={`category-options ${openUpward ? 'category-options-upward' : ''}`} role="listbox">
          {categories.map((category) => (
            <button type="button" role="option" aria-selected={category === value} className={`category-option ${category === value ? 'category-option-selected' : ''}`} key={category} onClick={() => { onChange({ target: { name: 'category', value: category } }); setIsOpen(false) }}>
              {category}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

function ProjectBrand({ className = '' }) {
  return (
    <div className={`project-brand ${className}`}>
      <img src="https://img.icons8.com/?size=100&id=8286&format=png&color=eaeaea" alt="" />
      <span>Stocks Master</span>
    </div>
  )
}

function Login({ onLogin, onRegister }) {
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (event) => {
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await axios.post(`${API_URL}/auth/login`, form)
      localStorage.setItem(TOKEN_KEY, response.data.access_token)
      onLogin(response.data.access_token)
    } catch (requestError) {
      setError(requestError.response?.data?.detail || 'Não foi possível entrar. Verifique seus dados.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="auth-container">
      <section className="auth-card">
        <ProjectBrand className="auth-brand" />
        <h1>Bem-vindo de volta</h1>
        <p className="auth-description">Entre na sua conta para acessar o estoque.</p>

        <form onSubmit={handleSubmit} className="auth-form">
          <label htmlFor="email">E-mail</label>
          <input
            id="email"
            type="email"
            name="email"
            placeholder="voce@empresa.com"
            value={form.email}
            onChange={handleChange}
            autoComplete="email"
            required
          />

          <label htmlFor="password">Senha</label>
          <input
            id="password"
            type="password"
            name="password"
            placeholder="Sua senha"
            value={form.password}
            onChange={handleChange}
            autoComplete="current-password"
            required
          />

          {error && <p className="form-error">{error}</p>}
          <button type="submit" disabled={loading}>
            {loading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>
        <button type="button" className="secondary-button" onClick={onRegister}>
          Criar uma conta
        </button>
      </section>
    </main>
  )
}

function Register({ onLogin, onBack }) {
  const [form, setForm] = useState({ email: '', password: '', store_name: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (event) => {
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await axios.post(`${API_URL}/auth/register`, {
        ...form,
        name: form.store_name,
      })
      localStorage.setItem(TOKEN_KEY, response.data.access_token)
      onLogin(response.data.access_token)
    } catch (requestError) {
      const detail = requestError.response?.data?.detail
      setError(detail === 'Email already registered'
        ? 'Este e-mail já está cadastrado. Use outro e-mail ou faça login.'
        : detail || 'Não foi possível criar a conta.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="auth-container">
      <section className="auth-card">
        <button type="button" className="back-button" onClick={onBack}>Voltar para o login</button>
        <ProjectBrand className="auth-brand" />
        <h1>Criar sua loja</h1>
        <p className="auth-description">Cadastre sua conta para começar a controlar o estoque.</p>

        <form onSubmit={handleSubmit} className="auth-form">
          <label htmlFor="store-name">Nome da loja</label>
          <input id="store-name" type="text" name="store_name" placeholder="Minha loja" value={form.store_name} onChange={handleChange} required />

          <label htmlFor="register-email">E-mail</label>
          <input id="register-email" type="email" name="email" placeholder="voce@empresa.com" value={form.email} onChange={handleChange} autoComplete="email" required />

          <label htmlFor="register-password">Senha</label>
          <input id="register-password" type="password" name="password" placeholder="Mínimo de 6 caracteres" value={form.password} onChange={handleChange} autoComplete="new-password" minLength="6" required />

          {error && <p className="form-error">{error}</p>}
          <button type="submit" disabled={loading}>
            {loading ? 'Criando conta...' : 'Criar conta'}
          </button>
        </form>
      </section>
    </main>
  )
}

function ProductModal({ form, isEditing, onChange, onSubmit, onClose }) {
  return (
    <div className="modal-backdrop" onMouseDown={onClose}>
      <section className="product-modal" role="dialog" aria-modal="true" aria-labelledby="product-modal-title" onMouseDown={(event) => event.stopPropagation()}>
        <div className="modal-heading">
          <div>
            <p className="label">Estoque</p>
            <h2 id="product-modal-title">{isEditing ? 'Editar produto' : 'Novo produto'}</h2>
          </div>
          <button type="button" className="modal-close" onClick={onClose} aria-label="Fechar modal">&times;</button>
        </div>

        <form onSubmit={onSubmit} className="product-form">
          <div className="form-field">
            <label htmlFor="product-name">Nome do produto</label>
            <input id="product-name" type="text" name="name" placeholder="Digite o nome do produto" value={form.name} onChange={onChange} required />
          </div>

          <div className="form-field">
            <label htmlFor="product-image">Link da imagem</label>
            <input id="product-image" type="url" name="image" placeholder="Cole o link da imagem" value={form.image} onChange={onChange} />
          </div>

          <div className="form-field">
            <label htmlFor="product-category">Categoria</label>
            <CategorySelect value={form.category} onChange={onChange} />
          </div>

          <div className="double-field">
            <div className="form-field">
              <label htmlFor="product-price">Valor</label>
              <input id="product-price" type="number" name="price" placeholder="0,00" min="0.01" step="0.01" value={form.price} onChange={onChange} required />
            </div>
            <div className="form-field">
              <label htmlFor="product-quantity">Quantidade</label>
              <input id="product-quantity" type="number" name="quantity" placeholder="0" min="0" value={form.quantity} onChange={onChange} required />
            </div>
          </div>

          <div className="modal-actions">
            <button type="button" className="cancel-button" onClick={onClose}>Cancelar</button>
            <button type="submit">{isEditing ? 'Salvar alterações' : 'Salvar produto'}</button>
          </div>
        </form>
      </section>
    </div>
  )
}

function DeleteConfirmationModal({ product, loading, error, onConfirm, onClose }) {
  return (
    <div className="modal-backdrop" onMouseDown={onClose}>
      <section className="product-modal confirmation-modal" role="dialog" aria-modal="true" aria-labelledby="delete-modal-title" onMouseDown={(event) => event.stopPropagation()}>
        <div className="modal-heading">
          <div>
            <p className="label">Atenção</p>
            <h2 id="delete-modal-title">Excluir produto?</h2>
          </div>
          <button type="button" className="modal-close" onClick={onClose} aria-label="Fechar modal">&times;</button>
        </div>

        <p className="confirmation-text">
          Tem certeza que deseja excluir <strong>{product.name}</strong>? Essa ação não pode ser desfeita.
        </p>
        {error && <p className="form-error">{error}</p>}

        <div className="modal-actions">
          <button type="button" className="cancel-button" onClick={onClose} disabled={loading}>Cancelar</button>
          <button type="button" className="delete-confirm-button" onClick={onConfirm} disabled={loading}>
            {loading ? 'Excluindo...' : 'Excluir produto'}
          </button>
        </div>
      </section>
    </div>
  )
}

function App() {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY))
  const [authPage, setAuthPage] = useState(() => window.location.pathname === '/cadastro' ? 'register' : 'login')
  const [storeName, setStoreName] = useState('Minha loja')
  const [products, setProducts] = useState([])
  const [search, setSearch] = useState('')
  const [form, setForm] = useState(emptyForm)
  const [isProductModalOpen, setIsProductModalOpen] = useState(false)
  const [editingProduct, setEditingProduct] = useState(null)
  const [productToDelete, setProductToDelete] = useState(null)
  const [deleteLoading, setDeleteLoading] = useState(false)
  const [deleteError, setDeleteError] = useState('')
  const [loading, setLoading] = useState(true)

  const fetchProducts = async () => {
    try {
      const response = await axios.get(`${API_URL}/products/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      setProducts(response.data)
    } catch (error) {
      console.error('Erro ao buscar produtos:', error)
      if (error.response?.status === 401) {
        handleLogout()
      }
    } finally {
      setLoading(false)
    }
  }

  const fetchProfile = async () => {
    try {
      const response = await axios.get(`${API_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      setStoreName(response.data.store_name)
    } catch (error) {
      console.error('Erro ao buscar perfil:', error)
      if (error.response?.status === 401) {
        handleLogout()
      }
    }
  }

  useEffect(() => {
    if (token) {
      if (window.location.pathname !== '/estoque') {
        window.history.replaceState({}, '', '/estoque')
      }
      fetchProfile()
      fetchProducts()
    } else {
      setLoading(false)
    }
  }, [token])

  const handleLogin = (accessToken) => {
    window.history.replaceState({}, '', '/estoque')
    setToken(accessToken)
  }

  const navigateAuth = (page) => {
    const path = page === 'register' ? '/cadastro' : '/'
    window.history.pushState({}, '', path)
    setAuthPage(page)
  }

  const handleLogout = () => {
    localStorage.removeItem(TOKEN_KEY)
    window.history.replaceState({}, '', '/')
    setToken(null)
    setStoreName('Minha loja')
    setProducts([])
    setForm(emptyForm)
    setEditingProduct(null)
    setIsProductModalOpen(false)
  }

  const openNewProductModal = () => {
    setForm(emptyForm)
    setEditingProduct(null)
    setIsProductModalOpen(true)
  }

  const openEditModal = (product) => {
    setForm({
      name: product.name,
      image: product.image || '',
      category: product.category || 'Outros',
      price: product.price,
      quantity: product.quantity,
    })
    setEditingProduct(product)
    setIsProductModalOpen(true)
  }

  const handleChange = (event) => {
    const { name, value } = event.target
    setForm((prev) => ({
      ...prev,
      [name]: name === 'price' || name === 'quantity' ? Number(value) : value,
    }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    try {
      const productData = {
        ...form,
        price: Number(form.price),
        quantity: Number(form.quantity),
      }
      const request = editingProduct
        ? axios.put(`${API_URL}/products/${editingProduct.id}`, productData, {
          headers: { Authorization: `Bearer ${token}` },
        })
        : axios.post(
          `${API_URL}/products/`,
          productData,
          { headers: { Authorization: `Bearer ${token}` } },
        )

      await request

      setEditingProduct(null)
      setForm(emptyForm)
      setIsProductModalOpen(false)
      fetchProducts()
    } catch (error) {
      console.error('Erro ao salvar produto:', error)
    }
  }

  const filteredProducts = products.filter((product) => {
    const term = search.trim().toLowerCase()
    if (!term) return true
    return [product.name, product.category, String(product.id)].some((value) => value?.toLowerCase().includes(term))
  })

  const openDeleteModal = (product) => {
    setDeleteError('')
    setProductToDelete(product)
  }

  const closeProductModal = () => {
    setIsProductModalOpen(false)
    setEditingProduct(null)
    setForm(emptyForm)
  }

  const closeDeleteModal = () => {
    if (!deleteLoading) {
      setProductToDelete(null)
      setDeleteError('')
    }
  }

  const handleDelete = async () => {
    setDeleteLoading(true)
    setDeleteError('')

    try {
      await axios.delete(`${API_URL}/products/${productToDelete.id}`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      setProducts((currentProducts) => currentProducts.filter((product) => product.id !== productToDelete.id))
      setProductToDelete(null)
    } catch (error) {
      setDeleteError(error.response?.data?.detail || 'Não foi possível excluir o produto.')
    } finally {
      setDeleteLoading(false)
    }
  }

  if (!token) {
    return authPage === 'register' ? (
      <Register onLogin={handleLogin} onBack={() => navigateAuth('login')} />
    ) : (
      <Login onLogin={handleLogin} onRegister={() => navigateAuth('register')} />
    )
  }

  return (
    <div className="app-container">
      <header className="site-header">
        <ProjectBrand className="brand" />
        <div className="header-actions">
          <span className="store-name">{storeName}</span>
          <button type="button" className="logout-button" onClick={handleLogout}>Sair</button>
        </div>
      </header>
      <div className="panel">
        <div className="product-toolbar">
          <button type="button" className="new-product-button" onClick={openNewProductModal}>+ Novo produto</button>
        </div>
        <section className="list-card">
          <div className="table-toolbar">
            <label htmlFor="product-search">Pesquisar produtos</label>
            <input id="product-search" type="search" placeholder="Nome, categoria ou ID" value={search} onChange={(event) => setSearch(event.target.value)} />
          </div>
          {loading ? (
            <p className="empty-state">Carregando...</p>
          ) : products.length === 0 ? (
            <p className="empty-state">Nenhum produto cadastrado.</p>
          ) : filteredProducts.length === 0 ? (
            <p className="empty-state">Nenhum produto encontrado.</p>
          ) : (
            <div className="table-scroll">
              <table className="product-table">
                <thead>
                  <tr>
                    <th>Imagem</th>
                    <th>Produto</th>
                    <th>ID</th>
                    <th>Categoria</th>
                    <th>Qtd</th>
                    <th>Preço Venda</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredProducts.map((product) => {
                    return (
                      <tr key={product.id}>
                        <td>
                          <div className="table-image-frame">
                            <img
                              src={product.image || 'https://via.placeholder.com/48x48?text=Produto'}
                              alt={product.name}
                            />
                          </div>
                        </td>
                        <td className="product-name-cell">{product.name}</td>
                        <td>{product.id}</td>
                        <td>{product.category}</td>
                        <td>{product.quantity} un</td>
                        <td>R$ {Number(product.price).toFixed(2)}</td>
                        <td>
                          <div className="table-actions">
                            <button type="button" aria-label={`Editar ${product.name}`} className="table-action table-action-edit" onClick={() => openEditModal(product)}>
                              <img src="https://img.icons8.com/?size=100&id=11762&format=png&color=eaeaea" alt="" />
                            </button>
                            <button type="button" aria-label={`Excluir ${product.name}`} className="table-action table-action-delete" onClick={() => openDeleteModal(product)}>
                              <img src="https://img.icons8.com/?size=100&id=FqXXiSW8IUD4&format=png&color=d5332c" alt="" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </div>
      {isProductModalOpen && (
        <ProductModal
          form={form}
          isEditing={Boolean(editingProduct)}
          onChange={handleChange}
          onSubmit={handleSubmit}
          onClose={closeProductModal}
        />
      )}
      {productToDelete && (
        <DeleteConfirmationModal
          product={productToDelete}
          loading={deleteLoading}
          error={deleteError}
          onConfirm={handleDelete}
          onClose={closeDeleteModal}
        />
      )}
    </div>
  )
}

export default App
