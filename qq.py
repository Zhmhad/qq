import abc
import asyncio
import os

class Barang(abc.ABC):
    def __init__(self, kode, nama, stok, harga):
        self.kode = kode
        self.nama = nama
        self.stok = stok
        self.harga = harga

    @abc.abstractmethod
    def kategori(self):
        pass

    def info(self):
        return f"- Kode Barang \t\t: {self.kode}  \n- Nama Barang \t\t: {self.nama}  \n- Kategori Barang \t: {self.kategori()}  \n- Stok \t\t\t: {self.stok} \n- Harga \t\t: {self.harga}"

class Elektronik(Barang):
    def kategori(self): 
        return "Elektronik"

class Pakaian(Barang):
    def kategori(self): 
        return "Baju & Celana"

class Buah(Barang):
    def kategori(self): 
        return "Buah-buahan"

class Susu(Barang):
    def kategori(self): 
        return "Susu"

class BarangTidakDitemukan(Exception): 
    pass

class StokTidakCukup(Exception): 
    pass

class DaftarBarang:
    def __init__(self):
        self._barang = []
        self._index = 0

    def tambah(self, barang):
        self._barang.append(barang)

    def cari(self, kode):
        for b in self._barang:
            if b.kode == kode:
                return b
        raise BarangTidakDitemukan(f"Barang dengan kode {kode} tidak ditemukan")

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self._barang):
            b = self._barang[self._index]
            self._index += 1
            return b
        raise StopIteration

def laporan_penjualan(transaksi):
    for t in transaksi:
        yield f"{t['nama']} - {t['jumlah']} pcs terjual - Total Rp{t['total']}"

async def cek_stok_menipis(daftar_barang):
    for b in daftar_barang:
        if b.stok <= 2:
            await asyncio.sleep(0)
            print(f"  Stok {b.nama} menipis! ({b.stok} tersisa)")

class PenjualanService:
    def __init__(self, daftar_barang):
        self.daftar = daftar_barang
        self.transaksi = []

    def jual(self, kode, jumlah):
        barang = self.daftar.cari(kode)
        if barang.stok < jumlah:
            raise StokTidakCukup(f"Stok {barang.nama} tidak cukup!")
        barang.stok -= jumlah
        total = barang.harga * jumlah
        self.transaksi.append({
            "nama": barang.nama,
            "jumlah": jumlah,
            "total": total
        })
        print(f"{jumlah} {barang.nama} berhasil dijual. Total: Rp{total:,}")

def menu():
    daftar = DaftarBarang()
    penjualan = PenjualanService(daftar)
    kategori_kata = {
    "1": ["HP", "Laptop", "TV", "Kulkas", "Kamera", "Speaker"],
    "2": ["Baju", "Celana", "Jaket", "Kaos", "Kemeja", "Rok"],
    "3": ["Apel", "Jeruk", "Pisang", "Pepaya", "Mangga", "Melon"],
    "4": ["Susu", "Dancow", "Frisian", "UHT", "Ultra", "Greenfield"]
}

    while True:
        os.system("cls")
        print("\n=== ZeroThree Trading ===")
        print("1. Tambah Barang")
        print("2. Jual Barang")
        print("3. Daftar Barang")
        print("4. Laporan Penjualan")
        print("5. Keluar")
        pilih = input("Pilih menu: ")

        if pilih == "1":
            os.system("cls")
            print("--- Tambah Barang ---")
            print("Kategori Barang: \n1.Elektronik  \n2.Pakaian  \n3.Buah  \n4.Susu")
            try:
                k = input("Pilih kategori (1-4): ").strip()
                if k not in kategori_kata:
                    raise ValueError("Kategori tidak valid!")
                
                if k in kategori_kata:
                    print("Jenis Barang :")
                    print(kategori_kata[k])

                kode = input("Kode barang (hanya angka): ").strip()
                if not kode.isdigit():
                    raise ValueError("Kode barang harus angka!")

                print("NOTE: Nama barang harus sesuai dengan Jenis barang!!!")
                if k == "1":
                    print("Inputan harus mengandung kata yang terdapat jenis barang, contoh : Hp Iphone 17 PRO dll")
                
                if k =="2":
                    print("Inputan harus mengandung kata yang terdapat jenis barang, contoh : Baju Hitam Polos dll")
                
                if k =="3":
                    print("Inputan harus mengandung kata yang terdapat jenis barang, contoh : Apel Hijau dll")
                    
                if k == "4":
                    print("Inputan harus mengandung kata yang terdapat jenis barang, contoh : Susu Sapi dll")
                
                nama = input("Nama barang : ").strip()
                cocok = any(kata.lower() in nama.lower() for kata in kategori_kata[k])
                if not cocok:
                    raise ValueError(f"Nama '{nama}' tidak sesuai dengan kategori yang dipilih ({k}).")

                kata_utama = [kata.lower() for kata in kategori_kata[k]]
                if len(nama.split()) == 1 or nama.lower() in kata_utama:
                    raise ValueError(f"Nama '{nama}' terlalu umum! Harus lebih spesifik, misalnya: '{kategori_kata[k][0]} tipe/model tertentu'.")


                stok_input = input("Stok awal: ").strip()
                harga_input = input("Harga: ").strip()
                if not (stok_input.isdigit() and harga_input.isdigit()):
                    raise ValueError("Stok dan harga harus angka!")

                stok = int(stok_input)
                harga = int(harga_input)
                if stok <= 0 or harga <= 0:
                    raise ValueError("Stok dan harga harus lebih dari 0!")

                if k == "1": 
                    barang = Elektronik(kode, nama, stok, harga)
                elif k == "2": 
                    barang = Pakaian(kode, nama, stok, harga)
                elif k == "3": 
                    barang = Buah(kode, nama, stok, harga)
                elif k == "4": 
                    barang = Susu(kode, nama, stok, harga)
                
                try:
                    daftar.cari(kode)
                    raise ValueError(f"Kode barang {kode} sudah digunakan!")
                except BarangTidakDitemukan:
                    pass
                
                daftar.tambah(barang)
                print(f" Barang '{nama}' berhasil ditambahkan ke kategori {k}!")
                input("Tekan enter untuk melanjutkan!!")

            except ValueError as e:
                print("X", e)
                input("Tekan enter untuk melanjutkan!!")
            except Exception as e:
                print("Terjadi kesalahan:", e)
                input("Tekan enter untuk melanjutkan!!")
                
        elif pilih == "2":
            os.system("cls")
            print("--- Penjualan Barang ---")
            if not daftar._barang:
                print("X Belum ada barang yang bisa dijual!")
                input("Tekan enter untuk melanjutkan!!")
                continue
            for b in daftar:
                print("="*40)
                print(b.info())
                print("="*40)
            try:
                kode = input("Masukkan kode barang: ")
                if not kode.isdigit():
                    raise ValueError("Kode barang harus angka!")
                
                jumlah_input = input("Jumlah dijual: ").strip()
                if not jumlah_input.isdigit():
                     raise ValueError("Jumlah harus angka!")
                jumlah = int(jumlah_input)
                
                penjualan.jual(kode, jumlah)
                input("Tekan enter untuk melanjutkan!!")
            except (BarangTidakDitemukan, StokTidakCukup) as e:
                print("X", e)
                input("Tekan enter untuk melanjutkan!!")
            
            except ValueError as e:
                print("X" , e)
                input("Tekan enter untuk melanjutkan!!")

        elif pilih == "3":
            os.system("cls")
            print("\n--- Daftar Barang ---")
            if not daftar._barang:
                print("Belum ada data barang.")
                input("Tekan enter untuk melanjutkan!!")
                continue
            for b in daftar:
                print("="*40)
                print(b.info())
                print("="*40)
            asyncio.run(cek_stok_menipis(daftar))
            input("Tekan enter untuk melanjutkan!!")

        elif pilih == "4":
            os.system("cls")
            print("\n--- Laporan Penjualan ---")
            if not penjualan.transaksi:
                print("Belum ada transaksi yang tercatat.")
            else:
                for line in laporan_penjualan(penjualan.transaksi):
                    print(line)
            input("Tekan enter untuk melanjutkan!!")
        elif pilih == "5":
            print("Terima kasih telah menggunakan aplikasi kami!!")
            break
        else:
            print("Menu tidak valid.")
menu()
#UAS
from abc import ABC, abstractmethod
from datetime import datetime

# ==================== DESIGN PATTERN 1 ====================
# 1. STRATEGY PATTERN
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass
    
    @abstractmethod
    def get_name(self):
        pass

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount):
        return f"✓ Pembayaran Rp{amount:,} via Kartu Kredit berhasil!"
    
    def get_name(self):
        return "Kartu Kredit"

class EWalletPayment(PaymentStrategy):
    def pay(self, amount):
        return f"✓ Pembayaran Rp{amount:,} via E-Wallet (OVO/GoPay) berhasil!"
    
    def get_name(self):
        return "E-Wallet"

class BankTransferPayment(PaymentStrategy):
    def pay(self, amount):
        return f"✓ Pembayaran Rp{amount:,} via Transfer Bank berhasil!"
    
    def get_name(self):
        return "Transfer Bank"

# 2. TEMPLATE PATTERN
class OrderTemplate(ABC):
    def process_order(self, order):
        print("\n" + "="*60)
        print("MEMPROSES PESANAN")
        print("="*60)
        self.validate_order(order)
        self.calculate_total(order)
        self.apply_discount(order)
        self.finalize_order(order)
        print("="*60)
        return order
    
    def validate_order(self, order):
        print(f"✓ Validasi pesanan untuk {order['customer']}")
    
    def calculate_total(self, order):
        total = sum(item['price'] * item['qty'] for item in order['items'])
        order['subtotal'] = total
        print(f"✓ Subtotal: Rp{total:,}")
    
    @abstractmethod
    def apply_discount(self, order):
        pass
    
    def finalize_order(self, order):
        print(f"✓ Total Akhir: Rp{order['total']:,}")
        print(f"✓ Pesanan selesai diproses!")

class RegularOrder(OrderTemplate):
    def apply_discount(self, order):
        order['total'] = order['subtotal']
        print("  Tidak ada diskon (Pelanggan Regular)")

class MemberOrder(OrderTemplate):
    def apply_discount(self, order):
        discount = order['subtotal'] * 0.10
        order['total'] = order['subtotal'] - discount
        print(f"✓ Diskon Member 10%: -Rp{discount:,}")

class VIPOrder(OrderTemplate):
    def apply_discount(self, order):
        discount = order['subtotal'] * 0.20
        order['total'] = order['subtotal'] - discount
        print(f"✓ Diskon VIP 20%: -Rp{discount:,}")

# ==================== DESIGN PATTERN 2 ====================
# 1. COMMAND PATTERN
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class AddItemCommand(Command):
    def __init__(self, cart, item):
        self.cart = cart
        self.item = item
    
    def execute(self):
        self.cart.append(self.item)
        print(f"✓ Ditambahkan: {self.item['name']} x{self.item['qty']} = Rp{self.item['price']*self.item['qty']:,}")
        return True

class RemoveItemCommand(Command):
    def __init__(self, cart, index):
        self.cart = cart
        self.index = index
    
    def execute(self):
        if 0 <= self.index < len(self.cart):
            removed = self.cart.pop(self.index)
            print(f"✓ Dihapus: {removed['name']}")
            return True
        print("✗ Item tidak ditemukan!")
        return False

class CheckoutCommand(Command):
    def __init__(self, cart, payment_strategy):
        self.cart = cart
        self.payment_strategy = payment_strategy
    
    def execute(self):
        total = sum(item['price'] * item['qty'] for item in self.cart)
        print(f"\n{'='*60}")
        print(f"CHECKOUT - Metode: {self.payment_strategy.get_name()}")
        print(f"{'='*60}")
        print(self.payment_strategy.pay(total))
        self.cart.clear()
        return total

# 2. ABSTRACT FACTORY PATTERN
class ProductFactory(ABC):
    @abstractmethod
    def create_product(self, name, price):
        pass

class ElectronicsFactory(ProductFactory):
    def create_product(self, name, price):
        return {
            'name': f"[Elektronik] {name}",
            'price': price,
            'category': 'Elektronik',
            'warranty': '1 Tahun'
        }

class FashionFactory(ProductFactory):
    def create_product(self, name, price):
        return {
            'name': f"[Fashion] {name}",
            'price': price,
            'category': 'Fashion',
            'warranty': '30 Hari'
        }

class FoodFactory(ProductFactory):
    def create_product(self, name, price):
        return {
            'name': f"[Makanan] {name}",
            'price': price,
            'category': 'Makanan',
            'warranty': 'Tidak ada'
        }

# ==================== SOLID PRINCIPLES ====================
# SRP - Single Responsibility Principle
class CartManager:
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        cmd = AddItemCommand(self.items, item)
        return cmd.execute()
    
    def remove_item(self, index):
        cmd = RemoveItemCommand(self.items, index)
        return cmd.execute()
    
    def get_total(self):
        return sum(item['price'] * item['qty'] for item in self.items)
    
    def show_cart(self):
        if not self.items:
            print("\n🛒 Keranjang kosong")
            return
        
        print("\n" + "="*60)
        print("🛒 KERANJANG BELANJA")
        print("="*60)
        for i, item in enumerate(self.items):
            print(f"{i+1}. {item['name']} x{item['qty']} @ Rp{item['price']:,} = Rp{item['price']*item['qty']:,}")
        print("-"*60)
        print(f"Total: Rp{self.get_total():,}")
        print("="*60)

# OCP - Open/Closed Principle
class DiscountCalculator:
    def __init__(self):
        self.strategies = {
            'regular': RegularOrder(),
            'member': MemberOrder(),
            'vip': VIPOrder()
        }
    
    def process(self, order_type, order):
        processor = self.strategies.get(order_type, RegularOrder())
        return processor.process_order(order)

# DIP - Dependency Inversion Principle
class OrderProcessor:
    def __init__(self, payment: PaymentStrategy, discount: OrderTemplate):
        self.payment = payment
        self.discount = discount
    
    def process(self, order):
        processed_order = self.discount.process_order(order)
        result = self.payment.pay(processed_order['total'])
        print(result)
        return processed_order

class TestRunner:
    @staticmethod
    def test_cart_manager():
        print("\n[TEST 1] CartManager - add_item() & get_total()")
        print("-" * 60)
        cart = CartManager()
        item1 = {'name': 'Laptop', 'price': 5000000, 'qty': 1}
        result = cart.add_item(item1)
        assert result == True, "Add item gagal!"
        
        item2 = {'name': 'Mouse', 'price': 150000, 'qty': 2}
        cart.add_item(item2)
        
        total = cart.get_total()
        expected = 5000000 + (150000 * 2)
        print(f"✓ Total: Rp{total:,} (Expected: Rp{expected:,})")
        assert total == expected, f"Total salah! Got {total}, expected {expected}"
        print("✓ TEST PASSED: add_item() & get_total() bekerja dengan benar!")
    
    @staticmethod
    def test_payment_strategy():
        print("\n[TEST 2] PaymentStrategy - pay() method")
        print("-" * 60)
        amount = 1000000
        
        cc = CreditCardPayment()
        result1 = cc.pay(amount)
        print(result1)
        assert "Kartu Kredit" in result1, "Payment method salah!"
        
        ew = EWalletPayment()
        result2 = ew.pay(amount)
        print(result2)
        assert "E-Wallet" in result2, "Payment method salah!"
        
        print("✓ TEST PASSED: pay() method bekerja untuk semua strategy!")
    
    @staticmethod
    def test_command_pattern():
        print("\n[TEST 3] Command Pattern - execute() method")
        print("-" * 60)
        cart = []
        item = {'name': 'Baju', 'price': 200000, 'qty': 1}
        
        add_cmd = AddItemCommand(cart, item)
        result = add_cmd.execute()
        assert result == True, "Add command gagal!"
        assert len(cart) == 1, "Item tidak masuk cart!"
        
        remove_cmd = RemoveItemCommand(cart, 0)
        result = remove_cmd.execute()
        assert result == True, "Remove command gagal!"
        assert len(cart) == 0, "Item tidak terhapus!"
        
        print("✓ TEST PASSED: Command execute() bekerja dengan benar!")
    
    @staticmethod
    def test_abstract_factory():
        print("\n[TEST 4] Abstract Factory - create_product() method")
        print("-" * 60)
        
        factory1 = ElectronicsFactory()
        product1 = factory1.create_product("TV", 3000000)
        print(f"Created: {product1['name']} - {product1['category']}")
        assert product1['category'] == 'Elektronik', "Kategori salah!"
        
        factory2 = FashionFactory()
        product2 = factory2.create_product("Sepatu", 500000)
        print(f"Created: {product2['name']} - {product2['category']}")
        assert product2['category'] == 'Fashion', "Kategori salah!"
        
        print("✓ TEST PASSED: create_product() bekerja untuk semua factory!")
    
    @staticmethod
    def test_template_pattern():
        print("\n[TEST 5] Template Pattern - process_order() method")
        print("-" * 60)
        
        order = {
            'customer': 'Test User',
            'items': [{'name': 'Produk Test', 'price': 1000000, 'qty': 1}]
        }
        
        member = MemberOrder()
        result = member.process_order(order.copy())
        expected = 1000000 * 0.9
        print(f"✓ Member total: Rp{result['total']:,} (Expected: Rp{expected:,})")
        assert result['total'] == expected, "Diskon salah!"
        
        print("✓ TEST PASSED: process_order() menghitung diskon dengan benar!")

# ==================== SOLID TESTING ====================
class SOLIDTester:
    @staticmethod
    def test_srp():
        print("\n[SOLID 1] SRP - Single Responsibility Principle")
        print("-" * 60)
        print("CartManager hanya bertanggung jawab mengelola keranjang")
        cart = CartManager()
        cart.add_item({'name': 'Item Test', 'price': 100000, 'qty': 1})
        cart.show_cart()
        print("✓ Tanggung jawab tunggal: manage cart items")
    
    @staticmethod
    def test_ocp():
        print("\n[SOLID 2] OCP - Open/Closed Principle")
        print("-" * 60)
        print("Bisa tambah diskon baru tanpa ubah kode existing")
        order = {
            'customer': 'User Test',
            'items': [{'name': 'Produk', 'price': 1000000, 'qty': 1}]
        }
        VIPOrder().process_order(order)
        print("✓ Extended dengan VIPOrder tanpa ubah base class")
    
    @staticmethod
    def test_lsp():
        print("\n[SOLID 3] LSP - Liskov Substitution Principle")
        print("-" * 60)
        print("Semua PaymentStrategy dapat disubstitusi satu sama lain")
        strategies = [CreditCardPayment(), EWalletPayment(), BankTransferPayment()]
        for strategy in strategies:
            print(f"→ {strategy.get_name()}: {strategy.pay(500000)}")
        print("✓ Semua subclass dapat menggantikan parent class")
    
    @staticmethod
    def test_isp():
        print("\n[SOLID 4] ISP - Interface Segregation Principle")
        print("-" * 60)
        print("Command interface hanya punya method yang diperlukan (execute)")
        cart = []
        item = {'name': 'Test', 'price': 100000, 'qty': 1}
        cmd = AddItemCommand(cart, item)
        cmd.execute()
        print("✓ Interface sederhana, tidak ada method yang tidak terpakai")
    
    @staticmethod
    def test_dip():
        print("\n[SOLID 5] DIP - Dependency Inversion Principle")
        print("-" * 60)
        print("High-level module bergantung pada abstraksi, bukan concrete class\n")
        order = {
            'customer': 'DIP Test',
            'items': [{'name': 'Produk', 'price': 1000000, 'qty': 1}]
        }
        
        print("Demo 1: CreditCard + Member Discount")
        processor1 = OrderProcessor(CreditCardPayment(), MemberOrder())
        processor1.process(order.copy())
        
        print("\nDemo 2: E-Wallet + VIP Discount (Dependency diganti)")
        processor2 = OrderProcessor(EWalletPayment(), VIPOrder())
        processor2.process(order.copy())
        
        print("\n✓ OrderProcessor tidak tahu concrete class yang dipakai")
        print("  Dependency di-inject dari luar (Dependency Injection)")

class InputValidator:
    @staticmethod
    def get_valid_choice(prompt, valid_choices):
        while True:
            choice = input(prompt).strip()
            if not choice:
                print("✗ Input tidak boleh kosong!")
                continue
            if choice in valid_choices:
                return choice
            print(f"✗ Pilihan tidak valid! Pilih salah satu: {', '.join(valid_choices)}")
    
    @staticmethod
    def get_valid_string(prompt, min_length=1):
        while True:
            value = input(prompt).strip()
            if not value:
                print("✗ Input tidak boleh kosong!")
                continue
            if len(value) < min_length:
                print(f"✗ Input minimal {min_length} karakter!")
                continue
            return value
    
    @staticmethod
    def get_valid_integer(prompt, min_value=1):
        while True:
            value = input(prompt).strip()
            if not value:
                print("✗ Input tidak boleh kosong!")
                continue
            try:
                num = int(value)
                if num < min_value:
                    print(f"✗ Nilai minimal {min_value}!")
                    continue
                return num
            except ValueError:
                print("✗ Input harus berupa angka!")

# ==================== MAIN APPLICATION ====================
class OnlineShopApp:
    def __init__(self):
        self.cart = CartManager()
        self.validator = InputValidator()
        self.factories = {
            '1': ElectronicsFactory(),
            '2': FashionFactory(),
            '3': FoodFactory()
        }
        self.payment_strategies = {
            '1': CreditCardPayment(),
            '2': EWalletPayment(),
            '3': BankTransferPayment()
        }
    
    def show_menu(self):
        print("\n" + "="*60)
        print("  RETAIL SHOP")
        print("="*60)
        print("1. Tambah Produk")
        print("2. Lihat Keranjang")
        print("3. Hapus Item")
        print("4. Checkout")
        print("5. Proses Pesanan dengan Diskon")
        print("6. Testing OOP - 5 Skenario Method Testing")
        print("7. Testing SOLID - 5 Prinsip SOLID")
        print("0. Keluar")
        print("="*60)
    
    def add_product(self):
        print("\nPilih Kategori:")
        print("1. Elektronik  2. Fashion  3. Makanan")
        
        choice = self.validator.get_valid_choice("Pilih (1-3): ", ['1', '2', '3'])
        factory = self.factories[choice]
        
        name = self.validator.get_valid_string("Nama produk: ")
        price = self.validator.get_valid_integer("Harga: ", min_value=1)
        qty = self.validator.get_valid_integer("Jumlah: ", min_value=1)
        
        product = factory.create_product(name, price)
        product['qty'] = qty
        self.cart.add_item(product)
    
    def checkout(self):
        if not self.cart.items:
            print("\n✗ Keranjang kosong!")
            return
        
        print("\nMetode Pembayaran:")
        print("1. Kartu Kredit  2. E-Wallet  3. Transfer Bank")
        
        choice = self.validator.get_valid_choice("Pilih (1-3): ", ['1', '2', '3'])
        strategy = self.payment_strategies[choice]
        
        cmd = CheckoutCommand(self.cart.items, strategy)
        cmd.execute()
    
    def process_order_with_discount(self):
        if not self.cart.items:
            print("\n✗ Keranjang kosong!")
            return
        
        print("\nTipe Pelanggan:")
        print("1. Regular (0%)  2. Member (10%)  3. VIP (20%)")
        
        choice = self.validator.get_valid_choice("Pilih (1-3): ", ['1', '2', '3'])
        customer_name = self.validator.get_valid_string("Nama: ")
        
        order = {
            'customer': customer_name,
            'items': self.cart.items.copy(),
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        calculator = DiscountCalculator()
        order_types = {'1': 'regular', '2': 'member', '3': 'vip'}
        order_type = order_types[choice]
        
        calculator.process(order_type, order)
        self.cart.items.clear()
    
    def remove_item_from_cart(self):
        self.cart.show_cart()
        if not self.cart.items:
            return
        
        max_index = len(self.cart.items)
        idx = self.validator.get_valid_integer(f"Hapus nomor (1-{max_index}): ", min_value=1)
        
        if idx > max_index:
            print(f"✗ Nomor tidak valid! Pilih antara 1-{max_index}")
            return
        
        self.cart.remove_item(idx - 1)
    
    def run_oop_tests(self):
        print("\n" + "="*60)
        print(" TESTING OOP - 5 SKENARIO METHOD TESTING")
        print("="*60)
        TestRunner.test_cart_manager()
        TestRunner.test_payment_strategy()
        TestRunner.test_command_pattern()
        TestRunner.test_abstract_factory()
        TestRunner.test_template_pattern()
        print("\n" + "="*60)
        print(" SEMUA TEST PASSED!")
        print("="*60)
        input("\nTekan Enter untuk kembali...")
    
    def run_solid_tests(self):
        print("\n" + "="*60)
        print("  TESTING SOLID - 5 PRINSIP SOLID")
        print("="*60)
        SOLIDTester.test_srp()
        SOLIDTester.test_ocp()
        SOLIDTester.test_lsp()
        SOLIDTester.test_isp()
        SOLIDTester.test_dip()
        print("\n" + "="*60)
        print(" SEMUA PRINSIP SOLID TERDEMONSTRASIKAN!")
        print("="*60)
        input("\nTekan Enter untuk kembali...")
    
    def run(self):
        while True:
            self.show_menu()
            choice = self.validator.get_valid_choice("\nPilih (0-7): ", 
                                                     ['0', '1', '2', '3', '4', '5', '6', '7'])
            
            if choice == '1':
                self.add_product()
            elif choice == '2':
                self.cart.show_cart()
            elif choice == '3':
                self.remove_item_from_cart()
            elif choice == '4':
                self.checkout()
            elif choice == '5':
                self.process_order_with_discount()
            elif choice == '6':
                self.run_oop_tests()
            elif choice == '7':
                self.run_solid_tests()
            elif choice == '0':
                print("\n Terima kasih! ")
                break

if __name__ == "__main__":
    app = OnlineShopApp()
    app.run()

#P9
from abc import ABC, abstractmethod 
from datetime import datetime

class Peserta(ABC):
    def __init__(self, nama: str, jenis_kelamin: str, no_hp: str):
        self.nama = nama
        self.jenis_kelamin = jenis_kelamin
        self.no_hp = no_hp

    @abstractmethod
    def get_identitas(self) -> str:
        """Setiap turunan wajib menampilkan identitas dengan format masing-masing"""
        pass

    @abstractmethod
    def get_peran(self) -> str:
        pass

class Mahasiswa(Peserta):
    def __init__(self, nim, nama, prodi, angkatan, jenis_kelamin, no_hp):
        super().__init__(nama, jenis_kelamin, no_hp)
        self.nim = nim
        self.prodi = prodi
        self.angkatan = angkatan

    def get_identitas(self):
        return (f"NIM {self.nim} | {self.nama} | {self.prodi} | "
                f"Angkatan {self.angkatan} | {self.jenis_kelamin} | {self.no_hp}")

    def get_peran(self):
        return "Mahasiswa"

class Dosen(Peserta):
    def __init__(self, nip, nama, jabatan, jenis_kelamin, no_hp):
        super().__init__(nama, jenis_kelamin, no_hp)
        self.nip = nip
        self.jabatan = jabatan

    def get_identitas(self):
        return (f"NIP {self.nip} | {self.nama} | {self.jabatan} | "
                f"{self.jenis_kelamin} | {self.no_hp}")

    def get_peran(self):
        return "Dosen"

class Absensi:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._daftar_hadir = []
            cls._instance._nama_acara = None
            cls._instance._tanggal = None
        return cls._instance

    def set_acara(self, nama_acara: str):
        self._nama_acara = nama_acara
        self._tanggal = datetime.now().strftime("%d-%m-%Y %H:%M")

    def tambah_kehadiran(self, peserta: Peserta):
        self._daftar_hadir.append(peserta)
        print(f"[INFO] {peserta.get_peran()} '{peserta.nama}' berhasil dicatat hadir.")

    def hitung_jumlah_pengunjung(self) -> int:
        return len(self._daftar_hadir)

    def hitung_per_peran(self):
        jumlah_mhs = sum(1 for p in self._daftar_hadir if isinstance(p, Mahasiswa))
        jumlah_dosen = sum(1 for p in self._daftar_hadir if isinstance(p, Dosen))
        return jumlah_mhs, jumlah_dosen

    def cetak_absensi(self):
        garis = "=" * 75
        print(garis)
        print(f"REKAP ABSENSI ACARA : {self._nama_acara}")
        print(f"Dicetak pada         : {self._tanggal}")
        print(garis)
        if not self._daftar_hadir:
            print("Belum ada peserta yang hadir.")
        else:
            for i, p in enumerate(self._daftar_hadir, start=1):
                print(f"{i}. ({p.get_peran()}) {p.get_identitas()}")
        print(garis)
        jml_mhs, jml_dosen = self.hitung_per_peran()
        print(f"Jumlah Mahasiswa Hadir : {jml_mhs}")
        print(f"Jumlah Dosen Hadir     : {jml_dosen}")
        print(f"TOTAL PENGUNJUNG       : {self.hitung_jumlah_pengunjung()}")
        print(garis)

class Zxyan:
    """
    Merepresentasikan mahasiswa yang bertugas melakukan
    rekap absensi pada sebuah acara kampus.
    """

    def __init__(self):
        # Mengambil instance Absensi (Singleton), bukan membuat objek baru
        self.absensi = Absensi()

    def buat_acara(self, nama_acara: str):
        self.absensi.set_acara(nama_acara)
        print(f"[Zxyan] Acara '{nama_acara}' telah dibuat dan siap menerima absensi.\n")

    def catat_kehadiran(self, peserta: Peserta):
        self.absensi.tambah_kehadiran(peserta)

    def cetak_laporan_absensi(self):
        print()
        self.absensi.cetak_absensi()

    def lihat_total_pengunjung(self):
        total = self.absensi.hitung_jumlah_pengunjung()
        print(f"\n[Zxyan] Total pengunjung acara sejauh ini: {total} orang.")
        return total
    
class Main:
    @staticmethod
    def run():
        petugas = Zxyan()
        petugas.buat_acara("Seminar Teknologi AI - Kampus Mikroskil")
        mhs1 = Mahasiswa("221111111", "Andi Pratama", "Teknik Informatika", 2022, "Laki-laki", "081200000001")
        mhs2 = Mahasiswa("221111112", "Melati Sari", "Sistem Informasi", 2022, "Perempuan", "081200000002")
        mhs3 = Mahasiswa("221111113", "Riko Saputra", "Teknik Informatika", 2023, "Laki-laki", "081200000003")
        dsn1 = Dosen("198501012010121001", "Dr. Budi Santoso, M.Kom", "Kepala Program Studi", "Laki-laki", "081300000001")
        dsn2 = Dosen("198702022012122002", "Dra. Rina Wijaya, M.T.", "Dosen Tetap", "Perempuan", "081300000002")
        for peserta in [mhs1, mhs2, mhs3, dsn1, dsn2]:
            petugas.catat_kehadiran(peserta)
        petugas.cetak_laporan_absensi()
        petugas.lihat_total_pengunjung()


if __name__ == "__main__":
    Main.run()

#P10
class Peserta(ABC):
    def __init__(self, nama: str, jenis_kelamin: str, no_hp: str):
        self.nama = nama
        self.jenis_kelamin = jenis_kelamin
        self.no_hp = no_hp

    @abstractmethod
    def get_identitas(self) -> str:
        """Setiap turunan wajib menampilkan identitas dengan format masing-masing"""
        pass

    @abstractmethod
    def get_peran(self) -> str:
        pass

    @abstractmethod
    def get_id(self) -> str:
        """Mengembalikan ID unik peserta (NIM untuk mahasiswa, NIP untuk dosen)"""
        pass

class Mahasiswa(Peserta):
    def __init__(self, nim, nama, prodi, angkatan, jenis_kelamin, no_hp):
        super().__init__(nama, jenis_kelamin, no_hp)
        self.nim = nim
        self.prodi = prodi
        self.angkatan = angkatan

    def get_identitas(self):
        return (f"NIM {self.nim} | {self.nama} | {self.prodi} | "
                f"Angkatan {self.angkatan} | {self.jenis_kelamin} | {self.no_hp}")

    def get_peran(self):
        return "Mahasiswa"

    def get_id(self):
        return self.nim

class Dosen(Peserta):
    def __init__(self, nip, nama, jabatan, jenis_kelamin, no_hp):
        super().__init__(nama, jenis_kelamin, no_hp)
        self.nip = nip
        self.jabatan = jabatan

    def get_identitas(self):
        return (f"NIP {self.nip} | {self.nama} | {self.jabatan} | "
                f"{self.jenis_kelamin} | {self.no_hp}")

    def get_peran(self):
        return "Dosen"

    def get_id(self):
        return self.nip

class Absensi:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._daftar_hadir = []      # urutan kehadiran (list)
            cls._instance._penyimpanan = {}        # tempat penyimpanan sementara: {id: peserta}
            cls._instance._nama_acara = None
            cls._instance._tanggal = None
        return cls._instance

    def set_acara(self, nama_acara: str):
        self._nama_acara = nama_acara
        self._tanggal = datetime.now().strftime("%d-%m-%Y %H:%M")

    def tambah_kehadiran(self, peserta: Peserta) -> bool:
        """Mencatat kehadiran. Mengembalikan False bila ID sudah pernah absen (mencegah duplikat)."""
        id_peserta = peserta.get_id()
        if id_peserta in self._penyimpanan:
            print(f"[PERINGATAN] {peserta.get_peran()} dengan ID '{id_peserta}' sudah tercatat hadir sebelumnya.")
            return False

        self._daftar_hadir.append(peserta)
        self._penyimpanan[id_peserta] = peserta  # simpan ke penyimpanan sementara
        print(f"[INFO] {peserta.get_peran()} '{peserta.nama}' berhasil dicatat hadir.")
        return True

    def cari_peserta(self, id_peserta: str):
        """Mencari data peserta berdasarkan NIM/NIP dari penyimpanan sementara. O(1) rata-rata."""
        return self._penyimpanan.get(id_peserta)

    def cek_kehadiran(self, id_peserta: str) -> bool:
        """Mengecek apakah ID tertentu sudah tercatat hadir atau belum."""
        return id_peserta in self._penyimpanan

    def hitung_jumlah_pengunjung(self) -> int:
        return len(self._daftar_hadir)

    def hitung_per_peran(self):
        jumlah_mhs = sum(1 for p in self._daftar_hadir if isinstance(p, Mahasiswa))
        jumlah_dosen = sum(1 for p in self._daftar_hadir if isinstance(p, Dosen))
        return jumlah_mhs, jumlah_dosen

    def cetak_absensi(self):
        garis = "=" * 75
        print(garis)
        print(f"REKAP ABSENSI ACARA : {self._nama_acara}")
        print(f"Dicetak pada         : {self._tanggal}")
        print(garis)
        if not self._daftar_hadir:
            print("Belum ada peserta yang hadir.")
        else:
            for i, p in enumerate(self._daftar_hadir, start=1):
                print(f"{i}. ({p.get_peran()}) {p.get_identitas()}")
        print(garis)
        jml_mhs, jml_dosen = self.hitung_per_peran()
        print(f"Jumlah Mahasiswa Hadir : {jml_mhs}")
        print(f"Jumlah Dosen Hadir     : {jml_dosen}")
        print(f"TOTAL PENGUNJUNG       : {self.hitung_jumlah_pengunjung()}")
        print(garis)

class Zxyan:
    """
    Merepresentasikan mahasiswa yang bertugas melakukan
    rekap absensi pada sebuah acara kampus, termasuk mencari
    dan mengecek data peserta dari penyimpanan sementara.
    """

    def __init__(self):
        self.absensi = Absensi()

    def buat_acara(self, nama_acara: str):
        self.absensi.set_acara(nama_acara)
        print(f"[Zxyan] Acara '{nama_acara}' telah dibuat dan siap menerima absensi.\n")

    def catat_kehadiran(self, peserta: Peserta):
        self.absensi.tambah_kehadiran(peserta)

    def cari_data_peserta(self, id_peserta: str):
        hasil = self.absensi.cari_peserta(id_peserta)
        print(f"\n[Zxyan] Mencari data dengan ID '{id_peserta}' ...")
        if hasil:
            print(f"  -> Ditemukan: ({hasil.get_peran()}) {hasil.get_identitas()}")
        else:
            print("  -> Data tidak ditemukan dalam penyimpanan sementara.")
        return hasil

    def cek_status_kehadiran(self, id_peserta: str):
        status = self.absensi.cek_kehadiran(id_peserta)
        keterangan = "SUDAH hadir" if status else "BELUM tercatat hadir"
        print(f"[Zxyan] Status ID '{id_peserta}': {keterangan}.")
        return status

    def cetak_laporan_absensi(self):
        print()
        self.absensi.cetak_absensi()

    def lihat_total_pengunjung(self):
        total = self.absensi.hitung_jumlah_pengunjung()
        print(f"\n[Zxyan] Total pengunjung acara sejauh ini: {total} orang.")
        return total

class Main:
    @staticmethod
    def run():
        petugas = Zxyan()
        petugas.buat_acara("Seminar Teknologi AI - Kampus Mikroskil")
        mhs1 = Mahasiswa("221111111", "Andi Pratama", "Teknik Informatika", 2022, "Laki-laki", "081200000001")
        mhs2 = Mahasiswa("221111112", "Melati Sari", "Sistem Informasi", 2022, "Perempuan", "081200000002")
        mhs3 = Mahasiswa("221111113", "Riko Saputra", "Teknik Informatika", 2023, "Laki-laki", "081200000003")
        dsn1 = Dosen("198501012010121001", "Dr. Budi Santoso, M.Kom", "Kepala Program Studi", "Laki-laki", "081300000001")
        dsn2 = Dosen("198702022012122002", "Dra. Rina Wijaya, M.T.", "Dosen Tetap", "Perempuan", "081300000002")
        for peserta in [mhs1, mhs2, mhs3, dsn1, dsn2]:
            petugas.catat_kehadiran(peserta)
        petugas.catat_kehadiran(mhs1)
        petugas.cetak_laporan_absensi()
        petugas.lihat_total_pengunjung()
        petugas.cari_data_peserta("221111112")   # ada (Melati Sari)
        petugas.cari_data_peserta("199999999")   # tidak ada
        petugas.cek_status_kehadiran("198501012010121001")  # sudah hadir
        petugas.cek_status_kehadiran("221111199")           # belum hadir


if __name__ == "__main__":
    Main.run()

#P11
from abc import ABC, abstractmethod

class KelasKalkulus:
    """Kelas A - T1/L2 - Dosen mengajarkan kalkulus"""

    def __init__(self, kode_ruangan, nama_dosen):
        self.kode_ruangan = kode_ruangan
        self.nama_dosen = nama_dosen

    def hitung_proses(self):
        return [
            "Menjelaskan konsep limit dan turunan fungsi",
            "Menghitung integral tak tentu & tertentu",
            "Membahas latihan soal kalkulus lanjutan",
        ]


class KelasPemrograman:
    """Kelas B - T3/L2 - Dosen mengajarkan pemrograman"""

    def __init__(self, kode_ruangan, nama_dosen):
        self.kode_ruangan = kode_ruangan
        self.nama_dosen = nama_dosen

    def jalankan_proses_praktikum(self):
        return [
            "Menjelaskan struktur perulangan (looping)",
            "Praktik penulisan fungsi dan debugging program",
            "Studi kasus penerapan Object Oriented Programming",
        ]


class KelasBahasaInggris:
    """Kelas C - T5/L2 - Dosen mengajarkan Bahasa Inggris"""

    def __init__(self, kode_ruangan, nama_dosen):
        self.kode_ruangan = kode_ruangan
        self.nama_dosen = nama_dosen

    def ajarkan_formula(self):
        return [
            "Menjelaskan formula tenses (Present, Past, Future)",
            "Latihan menyusun kalimat menggunakan grammar formula",
            "Diskusi & praktik percakapan (speaking practice)",
        ]

class IKelasInfo(ABC):
    @abstractmethod
    def get_nama_kelas(self) -> str:
        pass

    @abstractmethod
    def get_kode_ruangan(self) -> str:
        pass

    @abstractmethod
    def get_nama_dosen(self) -> str:
        pass

    @abstractmethod
    def get_daftar_proses(self) -> list:
        pass

class AdapterKalkulus(IKelasInfo):
    def __init__(self, kelas_asli: KelasKalkulus):
        self._kelas = kelas_asli

    def get_nama_kelas(self):
        return "Kelas A - Kalkulus"

    def get_kode_ruangan(self):
        return self._kelas.kode_ruangan

    def get_nama_dosen(self):
        return self._kelas.nama_dosen

    def get_daftar_proses(self):
        return self._kelas.hitung_proses()          # <- adaptasi nama method


class AdapterPemrograman(IKelasInfo):
    def __init__(self, kelas_asli: KelasPemrograman):
        self._kelas = kelas_asli

    def get_nama_kelas(self):
        return "Kelas B - Pemrograman"

    def get_kode_ruangan(self):
        return self._kelas.kode_ruangan

    def get_nama_dosen(self):
        return self._kelas.nama_dosen

    def get_daftar_proses(self):
        return self._kelas.jalankan_proses_praktikum()  # <- adaptasi nama method


class AdapterBahasaInggris(IKelasInfo):
    def __init__(self, kelas_asli: KelasBahasaInggris):
        self._kelas = kelas_asli

    def get_nama_kelas(self):
        return "Kelas C - Bahasa Inggris"

    def get_kode_ruangan(self):
        return self._kelas.kode_ruangan

    def get_nama_dosen(self):
        return self._kelas.nama_dosen

    def get_daftar_proses(self):
        return self._kelas.ajarkan_formula()          # <- adaptasi nama method

class Zxyan:
    """
    Merepresentasikan resepsionis yang merekap absensi dari
    beberapa kelas berbeda. Berkat Adapter, Zxyan hanya perlu
    berinteraksi dengan interface IKelasInfo yang seragam, tanpa
    peduli method asli tiap kelas.
    """

    def __init__(self):
        self._daftar_kelas: list[IKelasInfo] = []

    def daftarkan_kelas(self, kelas_info: IKelasInfo):
        self._daftar_kelas.append(kelas_info)
        print(f"[Zxyan] '{kelas_info.get_nama_kelas()}' berhasil didaftarkan untuk direkap.")

    def cetak_rekap_absensi(self):
        garis = "=" * 75
        print(f"\n{garis}")
        print("REKAP ABSENSI SELURUH KELAS")
        print(garis)
        for kelas in self._daftar_kelas:
            print(f"Nama Kelas   : {kelas.get_nama_kelas()}")
            print(f"Ruangan      : {kelas.get_kode_ruangan()}")
            print(f"Dosen        : {kelas.get_nama_dosen()}")
            print("Proses yang dilakukan :")
            for i, proses in enumerate(kelas.get_daftar_proses(), start=1):
                print(f"   {i}. {proses}")
            print("-" * 75)
        print(f"Total kelas yang direkap : {len(self._daftar_kelas)} kelas")
        print(garis)

if __name__ == "__main__":
    resepsionis = Zxyan()
    kelas_a = KelasKalkulus(kode_ruangan="T1/L2", nama_dosen="Dr. Hartono, M.Si")
    kelas_b = KelasPemrograman(kode_ruangan="T3/L2", nama_dosen="Ir. Yohanes Susanto, M.Kom")
    kelas_c = KelasBahasaInggris(kode_ruangan="T5/L2", nama_dosen="Dra. Melinda Tan, M.Pd")
    resepsionis.daftarkan_kelas(AdapterKalkulus(kelas_a))
    resepsionis.daftarkan_kelas(AdapterPemrograman(kelas_b))
    resepsionis.daftarkan_kelas(AdapterBahasaInggris(kelas_c))
    resepsionis.cetak_rekap_absensi()

#P12
"""
Task-01 : Rincian & Total Biaya Pendaftaran Mahasiswa Kampus Mikroskil
Design Pattern : COMPOSITE

Alasan pemilihan pattern:
Perhatikan struktur data biaya pada soal:
  - Uang Pendaftaran        -> item TUNGGAL
  - Uang Kuliah Pertama     -> item TUNGGAL
  - Uang MPT                -> ini bukan satu item, tapi sebuah KELOMPOK
        - Uang Training
        - Uang Penginapan
        - Uang Konsumsi

Jadi ada dua jenis "biaya": biaya tunggal (leaf) dan biaya yang
sebenarnya adalah gabungan dari beberapa biaya lain (composite/group).
Kesulitannya: agar semua biaya (baik yang tunggal maupun yang berupa
kelompok bertingkat) bisa DIJUMLAHKAN DENGAN BENAR tanpa harus menulis
logika khusus ("kalau ini grup, buka isinya dulu, kalau bukan, langsung
ambil nilainya") di setiap tempat.

Composite Pattern menyelesaikan ini dengan membuat leaf (BiayaItem) dan
group (BiayaGroup) sama-sama mengimplementasikan interface yang sama
(Biaya) dengan method get_total(). Pada BiayaGroup, get_total() akan
memanggil get_total() setiap anaknya secara rekursif -- anak tersebut
boleh berupa BiayaItem biasa ATAUPUN BiayaGroup lain. Dengan begitu,
client (bagian pendaftaran) cukup memanggil root.get_total() satu kali
untuk mendapatkan total keseluruhan biaya, sekaligus bisa menampilkan
rincian setiap tingkatannya.
"""

from abc import ABC, abstractmethod
class Biaya(ABC):
    def __init__(self, nama: str):
        self.nama = nama

    @abstractmethod
    def get_total(self) -> float:
        """Mengembalikan total nominal biaya (rekursif jika berupa grup)"""
        pass

    @abstractmethod
    def tampilkan(self, indent: int = 0):
        """Menampilkan rincian biaya, mendukung tampilan berjenjang"""
        pass

class BiayaItem(Biaya):
    def __init__(self, nama: str, nominal: float):
        super().__init__(nama)
        self.nominal = nominal

    def get_total(self) -> float:
        return self.nominal

    def tampilkan(self, indent: int = 0):
        spasi = "   " * indent
        print(f"{spasi}- {self.nama:<25}: {format_rupiah(self.nominal)}")

class BiayaGroup(Biaya):
    def __init__(self, nama: str):
        super().__init__(nama)
        self._anak: list[Biaya] = []

    def tambah(self, biaya: Biaya):
        self._anak.append(biaya)
        return self  

    def get_total(self) -> float:
        return sum(anak.get_total() for anak in self._anak)

    def tampilkan(self, indent: int = 0):
        spasi = "   " * indent
        print(f"{spasi}{self.nama} :")
        for anak in self._anak:
            anak.tampilkan(indent + 1)
        if indent > 0:
            print(f"{spasi}  Subtotal {self.nama:<15}: {format_rupiah(self.get_total())}")


def format_rupiah(nominal: float) -> str:
    """Format angka menjadi Rp X.XXX.XXX,00 (gaya format Indonesia)"""
    return "Rp " + f"{nominal:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")

class Zxyan:
    """
    Merepresentasikan bagian pendaftaran Mikroskil yang mengelola
    rincian biaya pendaftaran mahasiswa dalam bentuk struktur
    Composite (biaya tunggal & kelompok biaya).
    """

    def __init__(self, nama_rincian: str):
        self._root = BiayaGroup(nama_rincian)

    def tambah_biaya(self, biaya: Biaya):
        self._root.tambah(biaya)
        print(f"[Zxyan] '{biaya.nama}' berhasil ditambahkan ke rincian biaya pendaftaran.")

    def cetak_rincian(self):
        garis = "=" * 60
        print(f"\n{garis}")
        self._root.tampilkan()
        print(garis)

    def tampilkan_total(self):
        total = self._root.get_total()
        print(f"TOTAL SELURUH BIAYA PENDAFTARAN : {format_rupiah(total)}")
        print("=" * 60)
        return total

if __name__ == "__main__":
    zxyan = Zxyan("Rincian Biaya Pendaftaran Mahasiswa Baru")
    zxyan.tambah_biaya(BiayaItem("Uang Pendaftaran", 200_000))
    zxyan.tambah_biaya(BiayaItem("Uang Kuliah Pertama", 1_500_000))
    uang_mpt = BiayaGroup("Uang MPT")
    uang_mpt.tambah(BiayaItem("Uang Training", 100_000))
    uang_mpt.tambah(BiayaItem("Uang Penginapan", 200_000))
    uang_mpt.tambah(BiayaItem("Uang Konsumsi", 150_000))
    zxyan.tambah_biaya(uang_mpt)
    zxyan.cetak_rincian()
    zxyan.tampilkan_total()

#P13
"""
Task-01 (Pertemuan-01) : Sistem Rekap Absensi Acara Kampus Mikroskil
Kelas Utama    : Zxyan
Design Pattern : SINGLETON (pada kelas Absensi)

Catatan untuk Pertemuan Pengujian (Unit Testing):
Karena Absensi adalah Singleton (satu instance dipakai bersama selama
program berjalan), data hasil test sebelumnya bisa "nyangkut" dan
mempengaruhi test berikutnya. Untuk itu ditambahkan satu method kecil,
`Absensi.reset_instance()`, KHUSUS untuk keperluan pengujian -- supaya
setiap test bisa mulai dari kondisi bersih (isolated test).
Tidak ada perubahan pada logika bisnis / perhitungan aslinya.
"""

from abc import ABC, abstractmethod
from datetime import datetime

class Peserta(ABC):
    def __init__(self, nama: str, jenis_kelamin: str, no_hp: str):
        self.nama = nama
        self.jenis_kelamin = jenis_kelamin
        self.no_hp = no_hp

    @abstractmethod
    def get_identitas(self) -> str:
        pass

    @abstractmethod
    def get_peran(self) -> str:
        pass

class Mahasiswa(Peserta):
    def __init__(self, nim, nama, prodi, angkatan, jenis_kelamin, no_hp):
        super().__init__(nama, jenis_kelamin, no_hp)
        self.nim = nim
        self.prodi = prodi
        self.angkatan = angkatan

    def get_identitas(self):
        return (f"NIM {self.nim} | {self.nama} | {self.prodi} | "
                f"Angkatan {self.angkatan} | {self.jenis_kelamin} | {self.no_hp}")

    def get_peran(self):
        return "Mahasiswa"

class Dosen(Peserta):
    def __init__(self, nip, nama, jabatan, jenis_kelamin, no_hp):
        super().__init__(nama, jenis_kelamin, no_hp)
        self.nip = nip
        self.jabatan = jabatan

    def get_identitas(self):
        return (f"NIP {self.nip} | {self.nama} | {self.jabatan} | "
                f"{self.jenis_kelamin} | {self.no_hp}")

    def get_peran(self):
        return "Dosen"

class Absensi:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._daftar_hadir = []
            cls._instance._nama_acara = None
            cls._instance._tanggal = None
        return cls._instance

    @classmethod
    def reset_instance(cls):
        """KHUSUS UNTUK TESTING: mengosongkan instance Singleton agar
        setiap unit test bisa berjalan dengan kondisi awal yang bersih."""
        cls._instance = None

    def set_acara(self, nama_acara: str):
        self._nama_acara = nama_acara
        self._tanggal = datetime.now().strftime("%d-%m-%Y %H:%M")

    def tambah_kehadiran(self, peserta: Peserta):
        self._daftar_hadir.append(peserta)
        print(f"[INFO] {peserta.get_peran()} '{peserta.nama}' berhasil dicatat hadir.")

    def hitung_jumlah_pengunjung(self) -> int:
        return len(self._daftar_hadir)

    def hitung_per_peran(self):
        jumlah_mhs = sum(1 for p in self._daftar_hadir if isinstance(p, Mahasiswa))
        jumlah_dosen = sum(1 for p in self._daftar_hadir if isinstance(p, Dosen))
        return jumlah_mhs, jumlah_dosen

    def cetak_absensi(self):
        garis = "=" * 75
        print(garis)
        print(f"REKAP ABSENSI ACARA : {self._nama_acara}")
        print(f"Dicetak pada         : {self._tanggal}")
        print(garis)
        if not self._daftar_hadir:
            print("Belum ada peserta yang hadir.")
        else:
            for i, p in enumerate(self._daftar_hadir, start=1):
                print(f"{i}. ({p.get_peran()}) {p.get_identitas()}")
        print(garis)
        jml_mhs, jml_dosen = self.hitung_per_peran()
        print(f"Jumlah Mahasiswa Hadir : {jml_mhs}")
        print(f"Jumlah Dosen Hadir     : {jml_dosen}")
        print(f"TOTAL PENGUNJUNG       : {self.hitung_jumlah_pengunjung()}")
        print(garis)


class Zxyan:
    def __init__(self):
        self.absensi = Absensi()

    def buat_acara(self, nama_acara: str):
        self.absensi.set_acara(nama_acara)
        print(f"[Zxyan] Acara '{nama_acara}' telah dibuat dan siap menerima absensi.\n")

    def catat_kehadiran(self, peserta: Peserta):
        self.absensi.tambah_kehadiran(peserta)

    def cetak_laporan_absensi(self):
        print()
        self.absensi.cetak_absensi()

    def lihat_total_pengunjung(self):
        total = self.absensi.hitung_jumlah_pengunjung()
        print(f"\n[Zxyan] Total pengunjung acara sejauh ini: {total} orang.")
        return total

class Main:
    @staticmethod
    def run():
        petugas = Zxyan()
        petugas.buat_acara("Seminar Teknologi AI - Kampus Mikroskil")

        mhs1 = Mahasiswa("221111111", "Andi Pratama", "Teknik Informatika", 2022, "Laki-laki", "081200000001")
        mhs2 = Mahasiswa("221111112", "Melati Sari", "Sistem Informasi", 2022, "Perempuan", "081200000002")
        mhs3 = Mahasiswa("221111113", "Riko Saputra", "Teknik Informatika", 2023, "Laki-laki", "081200000003")

        dsn1 = Dosen("198501012010121001", "Dr. Budi Santoso, M.Kom", "Kepala Program Studi", "Laki-laki", "081300000001")
        dsn2 = Dosen("198702022012122002", "Dra. Rina Wijaya, M.T.", "Dosen Tetap", "Perempuan", "081300000002")

        for peserta in [mhs1, mhs2, mhs3, dsn1, dsn2]:
            petugas.catat_kehadiran(peserta)

        petugas.cetak_laporan_absensi()
        petugas.lihat_total_pengunjung()


if __name__ == "__main__":
    Main.run()
#TEST
"""
Unit Test untuk Task-01 Pertemuan-01 : Sistem Rekap Absensi
Framework   : unittest (bawaan Python)

Fokus pengujian (sesuai soal):
Memastikan proses PERHITUNGAN jumlah pengunjung/mahasiswa yang datang
sudah SESUAI atau belum, dengan cara membandingkan:
  - hitung_jumlah_pengunjung()  -> total keseluruhan peserta yang hadir
  - hitung_per_peran()          -> rincian jumlah Mahasiswa & Dosen

Rancangan pengujian mencakup:
  1. Kondisi awal (belum ada peserta)           -> harus 0
  2. Penambahan hanya Mahasiswa                 -> jumlah sesuai
  3. Penambahan hanya Dosen                     -> jumlah sesuai
  4. Penambahan campuran Mahasiswa & Dosen      -> total & rincian sesuai
  5. Validasi konsistensi data:
     jumlah_mhs + jumlah_dosen HARUS SAMA DENGAN total pengunjung
     (mengecek data tidak "sesuai/tidak sesuai")
  6. Perilaku Singleton: Absensi() selalu mengacu ke instance yang sama,
     termasuk saat diakses lewat beberapa objek Zxyan berbeda.

Setiap test diisolasi dengan me-reset instance Singleton pada setUp(),
supaya data dari satu test tidak "bocor" ke test lainnya.
"""

import unittest
# from task01_absensi import Absensi, Mahasiswa, Dosen, Zxyan


class TestPerhitunganAbsensi(unittest.TestCase):
    def setUp(self):
        Absensi.reset_instance()
        self.absensi = Absensi()
        self.absensi.set_acara("Acara Uji Coba")
        self.mhs1 = Mahasiswa("221111111", "Andi Pratama", "Teknik Informatika", 2022, "Laki-laki", "081200000001")
        self.mhs2 = Mahasiswa("221111112", "Melati Sari", "Sistem Informasi", 2022, "Perempuan", "081200000002")
        self.mhs3 = Mahasiswa("221111113", "Riko Saputra", "Teknik Informatika", 2023, "Laki-laki", "081200000003")
        self.dsn1 = Dosen("198501012010121001", "Dr. Budi Santoso, M.Kom", "Kaprodi", "Laki-laki", "081300000001")
        self.dsn2 = Dosen("198702022012122002", "Dra. Rina Wijaya, M.T.", "Dosen Tetap", "Perempuan", "081300000002")

    def tearDown(self):
        Absensi.reset_instance()

    def test_kondisi_awal_belum_ada_peserta(self):
        self.assertEqual(self.absensi.hitung_jumlah_pengunjung(), 0)
        self.assertEqual(self.absensi.hitung_per_peran(), (0, 0))

    def test_hitung_hanya_mahasiswa(self):
        self.absensi.tambah_kehadiran(self.mhs1)
        self.absensi.tambah_kehadiran(self.mhs2)
        self.assertEqual(self.absensi.hitung_jumlah_pengunjung(), 2)
        jml_mhs, jml_dosen = self.absensi.hitung_per_peran()
        self.assertEqual(jml_mhs, 2)
        self.assertEqual(jml_dosen, 0)

    def test_hitung_hanya_dosen(self):
        self.absensi.tambah_kehadiran(self.dsn1)

        self.assertEqual(self.absensi.hitung_jumlah_pengunjung(), 1)
        jml_mhs, jml_dosen = self.absensi.hitung_per_peran()
        self.assertEqual(jml_mhs, 0)
        self.assertEqual(jml_dosen, 1)

    def test_hitung_campuran_mahasiswa_dan_dosen(self):
        for peserta in [self.mhs1, self.mhs2, self.mhs3, self.dsn1, self.dsn2]:
            self.absensi.tambah_kehadiran(peserta)

        self.assertEqual(self.absensi.hitung_jumlah_pengunjung(), 5)
        jml_mhs, jml_dosen = self.absensi.hitung_per_peran()
        self.assertEqual(jml_mhs, 3)
        self.assertEqual(jml_dosen, 2)

    def test_konsistensi_total_dengan_rincian_per_peran(self):
        for peserta in [self.mhs1, self.mhs2, self.dsn1]:
            self.absensi.tambah_kehadiran(peserta)
        total = self.absensi.hitung_jumlah_pengunjung()
        jml_mhs, jml_dosen = self.absensi.hitung_per_peran()
        self.assertEqual(
            total, jml_mhs + jml_dosen,
            "Data TIDAK SESUAI: total pengunjung tidak sama dengan "
            "jumlah mahasiswa + jumlah dosen"
        )

    def test_absensi_bersifat_singleton(self):
        absensi_lain = Absensi()
        self.assertIs(self.absensi, absensi_lain)
        self.absensi.tambah_kehadiran(self.mhs1)
        self.assertEqual(absensi_lain.hitung_jumlah_pengunjung(), 1)

    def test_zxyan_mengakses_absensi_singleton_yang_sama(self):
        petugas_1 = Zxyan()
        petugas_2 = Zxyan()
        petugas_1.catat_kehadiran(self.mhs1)
        petugas_2.catat_kehadiran(self.dsn1)
        self.assertEqual(petugas_1.lihat_total_pengunjung(), 2)
        self.assertEqual(petugas_2.lihat_total_pengunjung(), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)

#P14
"""
Task-01 (Pertemuan-01) - Refactor menerapkan SOLID : S (SRP) & O (OCP)
Kelas Utama    : Zxyan
Design Pattern : SINGLETON (pada kelas Absensi)

Ringkasan perubahan dari kode pertemuan-01 sebelumnya ada di bagian
paling bawah file ini (komentar penjelasan penerapan SRP & OCP).
"""

from abc import ABC, abstractmethod
from datetime import datetime


class Peserta(ABC):
    def __init__(self, nama: str, jenis_kelamin: str, no_hp: str):
        self.nama = nama
        self.jenis_kelamin = jenis_kelamin
        self.no_hp = no_hp

    @abstractmethod
    def get_identitas(self) -> str:
        pass

    @abstractmethod
    def get_peran(self) -> str:
        pass

class Mahasiswa(Peserta):
    def __init__(self, nim, nama, prodi, angkatan, jenis_kelamin, no_hp):
        super().__init__(nama, jenis_kelamin, no_hp)
        self.nim = nim
        self.prodi = prodi
        self.angkatan = angkatan

    def get_identitas(self):
        return (f"NIM {self.nim} | {self.nama} | {self.prodi} | "
                f"Angkatan {self.angkatan} | {self.jenis_kelamin} | {self.no_hp}")

    def get_peran(self):
        return "Mahasiswa"

class Dosen(Peserta):
    def __init__(self, nip, nama, jabatan, jenis_kelamin, no_hp):
        super().__init__(nama, jenis_kelamin, no_hp)
        self.nip = nip
        self.jabatan = jabatan

    def get_identitas(self):
        return (f"NIP {self.nip} | {self.nama} | {self.jabatan} | "
                f"{self.jenis_kelamin} | {self.no_hp}")

    def get_peran(self):
        return "Dosen"

class Absensi:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._daftar_hadir = []
            cls._instance._nama_acara = None
            cls._instance._tanggal = None
        return cls._instance

    @classmethod
    def reset_instance(cls):
        """Khusus untuk kebutuhan pengujian (unit testing)."""
        cls._instance = None

    def set_acara(self, nama_acara: str):
        self._nama_acara = nama_acara
        self._tanggal = datetime.now().strftime("%d-%m-%Y %H:%M")

    def tambah_kehadiran(self, peserta: Peserta):
        self._daftar_hadir.append(peserta)
        print(f"[INFO] {peserta.get_peran()} '{peserta.nama}' berhasil dicatat hadir.")

    def get_daftar_hadir(self) -> list:
        return self._daftar_hadir

    def get_nama_acara(self) -> str:
        return self._nama_acara

    def get_tanggal(self) -> str:
        return self._tanggal

    def hitung_jumlah_pengunjung(self) -> int:
        return len(self._daftar_hadir)

    def hitung_per_peran(self) -> dict:
        """
        (OCP) Dihitung berdasarkan nilai get_peran() milik tiap peserta,
        BUKAN dengan isinstance/if-else terhadap Mahasiswa & Dosen secara
        eksplisit. Hasilnya berupa dictionary, misalnya:
            {"Mahasiswa": 3, "Dosen": 2}
        Kalau suatu saat ada jenis peserta baru (misal Tamu/Staff) yang
        merupakan turunan dari Peserta, method ini TIDAK PERLU diubah
        sama sekali -- perannya akan otomatis muncul di dictionary.
        """
        rekap: dict = {}
        for peserta in self._daftar_hadir:
            peran = peserta.get_peran()
            rekap[peran] = rekap.get(peran, 0) + 1
        return rekap

class LaporanAbsensi:
    def __init__(self, absensi: Absensi):
        self._absensi = absensi

    def cetak(self):
        garis = "=" * 75
        print(f"\n{garis}")
        print(f"REKAP ABSENSI ACARA : {self._absensi.get_nama_acara()}")
        print(f"Dicetak pada         : {self._absensi.get_tanggal()}")
        print(garis)

        daftar_hadir = self._absensi.get_daftar_hadir()
        if not daftar_hadir:
            print("Belum ada peserta yang hadir.")
        else:
            for i, p in enumerate(daftar_hadir, start=1):
                print(f"{i}. ({p.get_peran()}) {p.get_identitas()}")
        print(garis)
        for peran, jumlah in self._absensi.hitung_per_peran().items():
            print(f"Jumlah {peran} Hadir : {jumlah}")
        print(f"TOTAL PENGUNJUNG : {self._absensi.hitung_jumlah_pengunjung()}")
        print(garis)


class Zxyan:
    def __init__(self):
        self.absensi = Absensi()
        self.laporan = LaporanAbsensi(self.absensi)

    def buat_acara(self, nama_acara: str):
        self.absensi.set_acara(nama_acara)
        print(f"[Zxyan] Acara '{nama_acara}' telah dibuat dan siap menerima absensi.\n")

    def catat_kehadiran(self, peserta: Peserta):
        self.absensi.tambah_kehadiran(peserta)

    def cetak_laporan_absensi(self):
        self.laporan.cetak()

    def lihat_total_pengunjung(self):
        total = self.absensi.hitung_jumlah_pengunjung()
        print(f"\n[Zxyan] Total pengunjung acara sejauh ini: {total} orang.")
        return total

class Main:
    @staticmethod
    def run():
        petugas = Zxyan()
        petugas.buat_acara("Seminar Teknologi AI - Kampus Mikroskil")

        mhs1 = Mahasiswa("221111111", "Andi Pratama", "Teknik Informatika", 2022, "Laki-laki", "081200000001")
        mhs2 = Mahasiswa("221111112", "Melati Sari", "Sistem Informasi", 2022, "Perempuan", "081200000002")
        mhs3 = Mahasiswa("221111113", "Riko Saputra", "Teknik Informatika", 2023, "Laki-laki", "081200000003")

        dsn1 = Dosen("198501012010121001", "Dr. Budi Santoso, M.Kom", "Kepala Program Studi", "Laki-laki", "081300000001")
        dsn2 = Dosen("198702022012122002", "Dra. Rina Wijaya, M.T.", "Dosen Tetap", "Perempuan", "081300000002")

        for peserta in [mhs1, mhs2, mhs3, dsn1, dsn2]:
            petugas.catat_kehadiran(peserta)

        petugas.cetak_laporan_absensi()
        petugas.lihat_total_pengunjung()


if __name__ == "__main__":
    Main.run()

# [S] SINGLE RESPONSIBILITY PRINCIPLE
# Sebelumnya, kelas Absensi mengerjakan DUA hal sekaligus: (1) menyimpan
# & menghitung data kehadiran, dan (2) memformat serta mencetak laporan
# ke layar (method cetak_absensi() yang panjang berisi urusan tampilan).
# Ini melanggar SRP karena Absensi punya lebih dari satu "alasan untuk
# berubah": berubah jika cara penyimpanan data berubah, ATAU berubah
# jika format laporan berubah.
#
# Refactor: tanggung jawab cetak/format dipisah ke kelas baru
# LaporanAbsensi. Sekarang:
#   - Absensi       -> hanya berubah jika cara menyimpan/menghitung
#                       data kehadiran berubah.
#   - LaporanAbsensi -> hanya berubah jika tampilan/format laporan
#                       berubah (misal ingin ekspor ke PDF/HTML nantinya
#                       cukup ubah/tambah kelas ini, tanpa menyentuh
#                       Absensi sama sekali).
#   - Zxyan          -> hanya berperan sebagai koordinator, mendelegasikan
#                       ke kedua kelas di atas, tidak melakukan logika
#                       penyimpanan maupun pencetakan sendiri.
#
# [O] OPEN/CLOSED PRINCIPLE
# Sebelumnya, hitung_per_peran() memakai isinstance(p, Mahasiswa) dan
# isinstance(p, Dosen) secara eksplisit. Kalau suatu saat ditambah jenis
# peserta baru (misalnya Tamu atau Staff), method tersebut TERPAKSA
# diubah (tambah kondisi isinstance baru) -> melanggar OCP karena kelas
# yang sudah jadi/teruji harus dibuka & diubah lagi.
#
# Refactor: hitung_per_peran() sekarang mengelompokkan peserta berdasarkan
# nilai balik get_peran() (yang wajib diimplementasikan setiap turunan
# Peserta) ke dalam sebuah dictionary, tanpa mengecek tipe class secara
# eksplisit. LaporanAbsensi.cetak() juga mencetak rincian tersebut dengan
# me-loop dictionary itu, bukan menulis baris "Jumlah Mahasiswa" dan
# "Jumlah Dosen" secara manual. Akibatnya, untuk MENAMBAH jenis peserta
# baru, kita CUKUP membuat class baru turunan Peserta (misal class Tamu
# (Peserta): ... get_peran(): return "Tamu") -- tanpa mengubah satu pun
# baris kode di Absensi maupun LaporanAbsensi. Kode sudah "terbuka untuk
# ekstensi, tertutup untuk modifikasi".
#
# CATATAN: Kelas Peserta sebagai abstract class juga sudah selaras
# dengan OCP sejak awal (struktur pertemuan-01 sudah benar di bagian
# ini) -- penambahan jenis peserta baru dilakukan dengan extend Peserta,
# bukan mengubah Peserta itu sendiri, sehingga bagian ini tidak perlu
# direfactor lebih lanjut.
# =====================================================================

#P15
"""
Task-01 (Pertemuan-01) - Refactor menerapkan SOLID : S (SRP) & O (OCP)
Kelas Utama    : Zxyan
Design Pattern : SINGLETON (pada kelas Absensi)

Ringkasan perubahan dari kode pertemuan-01 sebelumnya ada di bagian
paling bawah file ini (komentar penjelasan penerapan SRP & OCP).
"""

from abc import ABC, abstractmethod
from datetime import datetime
class Peserta(ABC):
    def __init__(self, nama: str, jenis_kelamin: str, no_hp: str):
        self.nama = nama
        self.jenis_kelamin = jenis_kelamin
        self.no_hp = no_hp

    @abstractmethod
    def get_identitas(self) -> str:
        pass

    @abstractmethod
    def get_peran(self) -> str:
        pass

class Mahasiswa(Peserta):
    def __init__(self, nim, nama, prodi, angkatan, jenis_kelamin, no_hp):
        super().__init__(nama, jenis_kelamin, no_hp)
        self.nim = nim
        self.prodi = prodi
        self.angkatan = angkatan

    def get_identitas(self):
        return (f"NIM {self.nim} | {self.nama} | {self.prodi} | "
                f"Angkatan {self.angkatan} | {self.jenis_kelamin} | {self.no_hp}")

    def get_peran(self):
        return "Mahasiswa"

class Dosen(Peserta):
    def __init__(self, nip, nama, jabatan, jenis_kelamin, no_hp):
        super().__init__(nama, jenis_kelamin, no_hp)
        self.nip = nip
        self.jabatan = jabatan

    def get_identitas(self):
        return (f"NIP {self.nip} | {self.nama} | {self.jabatan} | "
                f"{self.jenis_kelamin} | {self.no_hp}")

    def get_peran(self):
        return "Dosen"

class Absensi:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._daftar_hadir = []
            cls._instance._nama_acara = None
            cls._instance._tanggal = None
        return cls._instance

    @classmethod
    def reset_instance(cls):
        """Khusus untuk kebutuhan pengujian (unit testing)."""
        cls._instance = None

    def set_acara(self, nama_acara: str):
        self._nama_acara = nama_acara
        self._tanggal = datetime.now().strftime("%d-%m-%Y %H:%M")

    def tambah_kehadiran(self, peserta: Peserta):
        self._daftar_hadir.append(peserta)
        print(f"[INFO] {peserta.get_peran()} '{peserta.nama}' berhasil dicatat hadir.")

    def get_daftar_hadir(self) -> list:
        return self._daftar_hadir

    def get_nama_acara(self) -> str:
        return self._nama_acara

    def get_tanggal(self) -> str:
        return self._tanggal

    def hitung_jumlah_pengunjung(self) -> int:
        return len(self._daftar_hadir)

    def hitung_per_peran(self) -> dict:
        """
        (OCP) Dihitung berdasarkan nilai get_peran() milik tiap peserta,
        BUKAN dengan isinstance/if-else terhadap Mahasiswa & Dosen secara
        eksplisit. Hasilnya berupa dictionary, misalnya:
            {"Mahasiswa": 3, "Dosen": 2}
        Kalau suatu saat ada jenis peserta baru (misal Tamu/Staff) yang
        merupakan turunan dari Peserta, method ini TIDAK PERLU diubah
        sama sekali -- perannya akan otomatis muncul di dictionary.
        """
        rekap: dict = {}
        for peserta in self._daftar_hadir:
            peran = peserta.get_peran()
            rekap[peran] = rekap.get(peran, 0) + 1
        return rekap

class LaporanAbsensi:
    def __init__(self, absensi: Absensi):
        self._absensi = absensi

    def cetak(self):
        garis = "=" * 75
        print(f"\n{garis}")
        print(f"REKAP ABSENSI ACARA : {self._absensi.get_nama_acara()}")
        print(f"Dicetak pada         : {self._absensi.get_tanggal()}")
        print(garis)

        daftar_hadir = self._absensi.get_daftar_hadir()
        if not daftar_hadir:
            print("Belum ada peserta yang hadir.")
        else:
            for i, p in enumerate(daftar_hadir, start=1):
                print(f"{i}. ({p.get_peran()}) {p.get_identitas()}")
        print(garis)
        for peran, jumlah in self._absensi.hitung_per_peran().items():
            print(f"Jumlah {peran} Hadir : {jumlah}")
        print(f"TOTAL PENGUNJUNG : {self._absensi.hitung_jumlah_pengunjung()}")
        print(garis)

class Zxyan:
    def __init__(self):
        self.absensi = Absensi()
        self.laporan = LaporanAbsensi(self.absensi)

    def buat_acara(self, nama_acara: str):
        self.absensi.set_acara(nama_acara)
        print(f"[Zxyan] Acara '{nama_acara}' telah dibuat dan siap menerima absensi.\n")

    def catat_kehadiran(self, peserta: Peserta):
        self.absensi.tambah_kehadiran(peserta)

    def cetak_laporan_absensi(self):
        self.laporan.cetak()

    def lihat_total_pengunjung(self):
        total = self.absensi.hitung_jumlah_pengunjung()
        print(f"\n[Zxyan] Total pengunjung acara sejauh ini: {total} orang.")
        return total

class Main:
    @staticmethod
    def run():
        petugas = Zxyan()
        petugas.buat_acara("Seminar Teknologi AI - Kampus Mikroskil")
        mhs1 = Mahasiswa("221111111", "Andi Pratama", "Teknik Informatika", 2022, "Laki-laki", "081200000001")
        mhs2 = Mahasiswa("221111112", "Melati Sari", "Sistem Informasi", 2022, "Perempuan", "081200000002")
        mhs3 = Mahasiswa("221111113", "Riko Saputra", "Teknik Informatika", 2023, "Laki-laki", "081200000003")
        dsn1 = Dosen("198501012010121001", "Dr. Budi Santoso, M.Kom", "Kepala Program Studi", "Laki-laki", "081300000001")
        dsn2 = Dosen("198702022012122002", "Dra. Rina Wijaya, M.T.", "Dosen Tetap", "Perempuan", "081300000002")
        for peserta in [mhs1, mhs2, mhs3, dsn1, dsn2]:
            petugas.catat_kehadiran(peserta)
        petugas.cetak_laporan_absensi()
        petugas.lihat_total_pengunjung()
if __name__ == "__main__":
    Main.run()


# =====================================================================
# PENJELASAN PENERAPAN PRINSIP SOLID (S & O)
# =====================================================================
#
# [S] SINGLE RESPONSIBILITY PRINCIPLE
# Sebelumnya, kelas Absensi mengerjakan DUA hal sekaligus: (1) menyimpan
# & menghitung data kehadiran, dan (2) memformat serta mencetak laporan
# ke layar (method cetak_absensi() yang panjang berisi urusan tampilan).
# Ini melanggar SRP karena Absensi punya lebih dari satu "alasan untuk
# berubah": berubah jika cara penyimpanan data berubah, ATAU berubah
# jika format laporan berubah.
#
# Refactor: tanggung jawab cetak/format dipisah ke kelas baru
# LaporanAbsensi. Sekarang:
#   - Absensi       -> hanya berubah jika cara menyimpan/menghitung
#                       data kehadiran berubah.
#   - LaporanAbsensi -> hanya berubah jika tampilan/format laporan
#                       berubah (misal ingin ekspor ke PDF/HTML nantinya
#                       cukup ubah/tambah kelas ini, tanpa menyentuh
#                       Absensi sama sekali).
#   - Zxyan          -> hanya berperan sebagai koordinator, mendelegasikan
#                       ke kedua kelas di atas, tidak melakukan logika
#                       penyimpanan maupun pencetakan sendiri.
#
# [O] OPEN/CLOSED PRINCIPLE
# Sebelumnya, hitung_per_peran() memakai isinstance(p, Mahasiswa) dan
# isinstance(p, Dosen) secara eksplisit. Kalau suatu saat ditambah jenis
# peserta baru (misalnya Tamu atau Staff), method tersebut TERPAKSA
# diubah (tambah kondisi isinstance baru) -> melanggar OCP karena kelas
# yang sudah jadi/teruji harus dibuka & diubah lagi.
#
# Refactor: hitung_per_peran() sekarang mengelompokkan peserta berdasarkan
# nilai balik get_peran() (yang wajib diimplementasikan setiap turunan
# Peserta) ke dalam sebuah dictionary, tanpa mengecek tipe class secara
# eksplisit. LaporanAbsensi.cetak() juga mencetak rincian tersebut dengan
# me-loop dictionary itu, bukan menulis baris "Jumlah Mahasiswa" dan
# "Jumlah Dosen" secara manual. Akibatnya, untuk MENAMBAH jenis peserta
# baru, kita CUKUP membuat class baru turunan Peserta (misal class Tamu
# (Peserta): ... get_peran(): return "Tamu") -- tanpa mengubah satu pun
# baris kode di Absensi maupun LaporanAbsensi. Kode sudah "terbuka untuk
# ekstensi, tertutup untuk modifikasi".
#
# CATATAN: Kelas Peserta sebagai abstract class juga sudah selaras
# dengan OCP sejak awal (struktur pertemuan-01 sudah benar di bagian
# ini) -- penambahan jenis peserta baru dilakukan dengan extend Peserta,
# bukan mengubah Peserta itu sendiri, sehingga bagian ini tidak perlu
# direfactor lebih lanjut.
# =====================================================================

#DAA - M11
#1
def minFlowers(n, k, c):
    c.sort(reverse=True)
    friends = [0] * k
    totalCost = 0

    for i in range(n):
        friendIndex = i % k
        totalCost += (friends[friendIndex] + 1) * c[i]
        friends[friendIndex] += 1

    return totalCost


n, k = list(map(int, input().split()))
c = list(map(int, input().split()))

print('Bunga : ', minFlowers(n, k, c))
#2
n = int(input())
scores = []

for i in range(n):
    scores.append(int(input()))

candies = [1] * n

for i in range(1, n):
    if scores[i] > scores[i - 1]:
        candies[i] = candies[i - 1] + 1

for i in range(n - 2, -1, -1):
    if scores[i] > scores[i + 1]:
        candies[i] = max(candies[i], candies[i + 1] + 1)

total = sum(candies)
print(total)
#3
def getMinimumTime(n, m, seats):
    minimumTime = float('inf')

    for start in range(1, m + 1):
        longestWait = 0
        for i in range(n):
            waitTime = (seats[i] - start + m) % m
            longestWait = max(longestWait, waitTime)
        minimumTime = min(minimumTime, longestWait)

    return minimumTime


n, m = map(int, input().split())
seats = list(map(int, input().split()))
print(getMinimumTime(n, m, seats))

#DAA - M12
#1
def min_max_difference(total_elements, subset_size, array):
    if subset_size <= 1:
        return 0

    array.sort()
    minimum_difference = float('inf')

    for i in range(total_elements - subset_size + 1):
        current_difference = array[i + subset_size - 1] - array[i]
        minimum_difference = min(minimum_difference, current_difference)

    return minimum_difference


total_elements, subset_size = map(int, input().split())
array = list(map(int, input().split()))
print(min_max_difference(total_elements, subset_size, array))
#2
pattern = []

def checklights(length):
    if length <= 3:
        lights = input()
        return -1
    else:
        lights = input()
        counter = 3

        for i in range(length):
            if i < 3:
                pattern.append(lights[i])
            else:
                if pattern[i % 3] == lights[i]:
                    counter += 1

        print(counter)


n = int(input())
print(checklights(n))
#3
def getCustomerOrders():
    numCustomers = int(input())
    entries = []

    while len(entries) < numCustomers:
        orderTime, prepTime = map(int, input().split())
        finishTime = orderTime + prepTime
        customerNumber = len(entries) + 1
        entries.append((finishTime, customerNumber))

    return sorted(entries)


orderQueue = getCustomerOrders()

for i in range(len(orderQueue)):
    print(orderQueue[i][1], end=' ')

#DAA - M13
#1
num_edges = int(input())
graph = {}

for _ in range(num_edges):
    node = input()
    neighbors = input().split()
    graph[node] = neighbors

print()

for node in graph:
    if graph[node]:
        print(f'Tetangga dari {node} adalah ', end='')
        for neighbor in graph[node]:
            print(neighbor, end='')
            if neighbor != graph[node][-1]:
                print(', ', end='')
    else:
        print(f'{node} tidak ada tetangga ', end='')
    print()
#2
def calculateSum(line):
    return sum(line)


def exploreConnections(matrix, source, marked):
    queue = [source]
    marked[source] = True
    found = 0

    while len(queue) > 0:
        current = queue.pop(0)
        for i in range(len(matrix)):
            if matrix[current][i] == 1 and not marked[i]:
                marked[i] = True
                queue.append(i)
                found += 1

    return found


def captureMatrix(size):
    result = []
    for _ in range(size):
        row = list(map(int, input().split()))
        result.append(row)
    return result


def detectCeoNode(matrix):
    count = len(matrix)
    offlineNodes = []

    for idx in range(count):
        if calculateSum(matrix[idx]) == 0:
            offlineNodes.append(idx)
        else:
            mark = [False] * count
            reach = exploreConnections(matrix, idx, mark)
            if reach == 0:
                offlineNodes.append(idx)

    return offlineNodes
machineCount = int(input())
connectionMatrix = captureMatrix(machineCount)
unlinked = detectCeoNode(connectionMatrix)

if len(unlinked) == 0:
    print('Semua komputer terhubung')
else:
    print(f'Komputer {unlinked[0]+1} adalah komputer CEO')